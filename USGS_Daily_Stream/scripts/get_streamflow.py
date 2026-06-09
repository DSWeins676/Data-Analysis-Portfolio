import requests
import pandas as pd
import json
import logging
import sqlite3

# Configure pipeline logging
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Pipeline started")


# ------------------------------------------------------------------
# EXTRACT: Monitoring Location Data
# ------------------------------------------------------------------

location_url = "https://api.waterdata.usgs.gov/ogcapi/v0/collections/monitoring-locations/items"

# Pull stream monitoring locations in Albany County, NY
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

location_data = location_response.json()

# Save raw API response for auditing/debugging
with open("data/raw/monitoring_locations_raw.json", "w") as f:
    json.dump(location_data, f, indent=2)

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

# Flatten nested API response into row-based records
for feature in location_data["features"]:
    props = feature["properties"]
    geo = feature["geometry"]

    row = {}

    # Pull selected metadata fields
    for column in selected_location_columns:
        row[column] = props.get(column)

    # Split coordinates into separate columns
    row["latitude"] = geo["coordinates"][1]
    row["longitude"] = geo["coordinates"][0]

    location_records.append(row)

location_df = pd.DataFrame(location_records)

logging.info(f"Monitoring locations pulled: {len(location_df)}")


# ------------------------------------------------------------------
# EXTRACT: Streamflow Data
# ------------------------------------------------------------------

# Build a comma-separated list of site IDs for the streamflow request
site_ids = location_df["id"].tolist()
site_ids_param = ",".join(site_ids)

streamflow_url = "https://api.waterdata.usgs.gov/ogcapi/v0/collections/daily/items"

# Pull daily streamflow (parameter 00060) for all monitoring locations
streamflow_params = {
    "f": "json",
    "limit": 1000,
    "time": "2024-01-01/2024-12-31",
    "monitoring_location_id": site_ids_param,
    "parameter_code": "00060",
}

streamflow_response = requests.get(streamflow_url, params=streamflow_params)
streamflow_response.raise_for_status()

streamflow_data = streamflow_response.json()

# Save raw API response for auditing/debugging
with open("data/raw/streamflow_raw.json", "w") as f:
    json.dump(streamflow_data, f, indent=2)

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

# Flatten streamflow API response into row-based records
for feature in streamflow_data["features"]:
    props = feature["properties"]

    row = {}

    for column in selected_streamflow_columns:
        row[column] = props.get(column)

    streamflow_records.append(row)

streamflow_df = pd.DataFrame(streamflow_records)

# Convert time column to datetime and sort records
streamflow_df["time"] = pd.to_datetime(streamflow_df["time"])

streamflow_df.sort_values(
    by=["monitoring_location_id", "time"],
    inplace=True
)


# ------------------------------------------------------------------
# TRANSFORM: Determine Which Sites Returned Streamflow Data
# ------------------------------------------------------------------

# Sites included in the monitoring location request
requested_site_ids = set(location_df["id"])

# Sites that actually returned streamflow observations
if streamflow_df.empty:
    returned_site_ids = set()
else:
    returned_site_ids = set(
        streamflow_df["monitoring_location_id"]
        .dropna()
        .unique()
    )

# Split locations into:
# 1. Sites with streamflow data
# 2. Sites without streamflow data
locations_with_streamflow_df = location_df[
    location_df["id"].isin(returned_site_ids)
]

locations_without_streamflow_df = location_df[
    ~location_df["id"].isin(returned_site_ids)
]

logging.info(f"Streamflow rows pulled: {len(streamflow_df)}")
logging.info(f"Sites with streamflow data: {len(locations_with_streamflow_df)}")
logging.info(f"Sites without streamflow data: {len(locations_without_streamflow_df)}")


# ------------------------------------------------------------------
# LOAD: Export Processed Data
# ------------------------------------------------------------------

streamflow_df.to_csv("data/processed/streamflow.csv", index=False)

# Store processed datasets in SQLite
conn = sqlite3.connect("data/processed/streamflow.db")

locations_with_streamflow_df.to_sql(
    "monitoring_locations",
    conn,
    if_exists="replace",
    index=False
)

streamflow_df.to_sql(
    "daily_streamflow",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

logging.info("Pipeline finished")