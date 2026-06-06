import requests
import pandas as pd
import json


url = "https://api.waterdata.usgs.gov/ogcapi/v0/collections/monitoring-locations/items"

params = {
    "f": "json",
    "limit": 1000,
    "state_code": "36",
    "county_code": "001",
    "site_type": "Stream",
    "properties": "id,monitoring_location_name,agency_code,agency_name,site_type,state_name,county_name,hydrologic_unit_code",
}

response = requests.get(url, params=params)
response.raise_for_status()

data=response.json()

selected_columns = [
    "id",
    "monitoring_location_name",
    "agency_code",
    "agency_name",
    "site_type",
    "state_name",
    "county_name",
    "hydrologic_unit_code"
]

records = []

for feature in data["features"]:
    props = feature["properties"]
    geo = feature["geometry"]

    row = {}
    
    for column in selected_columns:
        row[column] = props.get(column)
    row["latitude"] = geo["coordinates"][1]
    row["longitude"] = geo["coordinates"][0]

    records.append(row)


df = pd.DataFrame(records)

print(df.head())
print(len(df))
