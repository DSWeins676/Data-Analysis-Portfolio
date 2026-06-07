import requests
import pandas as pd
import json


location_url = "https://api.waterdata.usgs.gov/ogcapi/v0/collections/monitoring-locations/items"

location_params = {
    "f": "json",
    "limit": 1000,
    "state_code": "36",
    "county_code": "001",
    "site_type": "Stream",
    "properties": "id,monitoring_location_name,agency_code,agency_name,site_type,state_name,county_name,hydrologic_unit_code",
}

location_response = requests.get(location_url, params=location_params)
location_response.raise_for_status()

location_data=location_response.json()

selected_location_columns = [
    "id",
    "monitoring_location_name",
    "agency_code",
    "agency_name",
    "site_type",
    "state_name",
    "county_name",
    "hydrologic_unit_code"
]

location_records = []

## Goes the the nesting level necessary to get properties and geometry and writes to list

for feature in location_data["features"]:
    props = feature["properties"]
    geo = feature["geometry"]

    row = {}
    
    for column in selected_location_columns:
        row[column] = props.get(column)
    row["latitude"] = geo["coordinates"][1]
    row["longitude"] = geo["coordinates"][0]

    location_records.append(row)


location_df = pd.DataFrame(location_records)
print(len(location_df))

site_ids = location_df["id"].tolist()
site_ids_param = ",".join(site_ids)

streamflow_url = "https://api.waterdata.usgs.gov/ogcapi/v0/collections/daily/items"

streamflow_params = {
    "f": "json",
    "limit" : 1000,
    "time": "2024-01-01/2024-12-31",
    "monitoring_location_id" : site_ids_param,
    "parameter_code" : "00060",
}

streamflow_response = requests.get(streamflow_url, params=streamflow_params)
streamflow_response.raise_for_status()

streamflow_data = streamflow_response.json()

selected_streamflow_columns = [
    "monitoring_location_id",
    "time",
    "parameter_code",
    "parameter_name",
    "value",
    "unit_of_measure",
    "statistic_id",
    "approval_status"
]

streamflow_records = []

## Goes the the nesting level necessary to get properties and geometry and writes to list

for feature in streamflow_data["features"]:
    props = feature["properties"]

    row = {}

    for column in selected_streamflow_columns:
        row[column] = props.get(column)

    streamflow_records.append(row)

streamflow_df = pd.DataFrame(streamflow_records)
pd.to_datetime(streamflow_df['time'])
streamflow_df.sort_values(by=['monitoring_location_id','time'], inplace= True)

# Sites we asked the API for
requested_site_ids = set(location_df["id"])

# Sites that actually came back in the streamflow data
if streamflow_df.empty:
    returned_site_ids = set()
else:
    returned_site_ids = set(streamflow_df["monitoring_location_id"].dropna().unique())

# Split locations into with-data and without-data groups
locations_with_streamflow_df = location_df[
    location_df["id"].isin(returned_site_ids)
]

locations_without_streamflow_df = location_df[
    ~location_df["id"].isin(returned_site_ids)
]

# Locations that returned streamflow data
locations_with_streamflow_df = location_df[
    location_df["id"].isin(returned_site_ids)
]


# Locations that did not return streamflow data
locations_without_streamflow_df = location_df[
    ~location_df["id"].isin(returned_site_ids)
]

print("Requested sites:", len(requested_site_ids))
print("Sites with streamflow data:", len(returned_site_ids))
print("Sites without streamflow data:", len(locations_without_streamflow_df))

streamflow_df.to_csv("USGS Daily Stream/data/streamflow.csv", index=False)