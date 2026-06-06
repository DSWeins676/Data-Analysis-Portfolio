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

site_id = "USGS-01359135"
#location_df.loc[20, "id"]

streamflow_url = "https://api.waterdata.usgs.gov/ogcapi/v0/collections/daily/items"

streamflow_params = {
    "f": "json",
    "time": "2025-06-01/2025-06-30",
    "monitoring_location_id" : site_id,
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

for feature in streamflow_data["features"]:
    props = feature["properties"]

    row = {}

    for column in selected_streamflow_columns:
        row[column] = props.get(column)

    streamflow_records.append(row)

streamflow_df = pd.DataFrame(streamflow_records)
pd.to_datetime(streamflow_df['time'])
streamflow_df.sort_values(by=['time'], inplace= True)

print(streamflow_df.head())