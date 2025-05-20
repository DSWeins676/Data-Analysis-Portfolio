# Income Driven: Exploring Relationships Between Vehicles and Household Income in New York State

Author: Daniel Weinstein

Date: April 16th, 2025

## Objectives
Personal vehicles are essential for both work and leisure, especially when public transportation is not readily available. However, vehicles also impose significant costs, in both purchase and upkeep, on their owners, and this burden is felt more for households/families in lower socioeconomic brackets. Using a combination of New York State Department of Motor Vehicles (DMV) vehicle registration data and demographic/economic data from the U.S. Census Bureau, this project seeks to explore trends in vehicle ownership as well as relationships between vehicles and socioeconomic indicators across geographic locations in New York State. This may reveal trends that guide further research and analysis directions about the state of vehicles in New York.

## Data Source 
The main source for this analysis is the "Vehicle, Snowmobile, and Boat Registrations" dataset, available through New York Open Data (https://data.ny.gov/Transportation/Vehicle-Snowmobile-and-Boat-Registrations/w4pv-hbkt/about_data). The New York State Department of Motor Vehicle (DMV) requires registration of personal and commercial cars, trucks, boats, snowmobiles, and so on. The registration ties with other important aspects of vehicle ownership, such as insurance coverage and vehicle inspection status, to provide a regulatory mechanism to ensure the suitability of a vehicle for the road and to tie it to a particular owner in a particular state. This dataset was downloaded as a .csv file from NY Open Data, excluding boat and snowmobile registrations (Record Type = VEH)

Each row represents a unique registration, indicating the type of record (vehicle, boat, snowmobile, etc.), information about the vehicle itself, the city/state/county in which it is registered, and whether there are outstanding violations on the registration record.

The other main source of information was the 2023 American Community Survey 5-Year Estimates from the United States Census Bureau. Total Population was taken from Table S0101 - Age and Sex - and median household income was taken from Table S1903 - Median Income in the Past 12 Months (in 2023 Inflation-Adjusted Dollars). These were accessed via queries at https://data.census.gov, filtering by all counties in New York State. Due to significant formatting issues when downloading .csv files from this website, plus the small size of the dataset, this data was mostly merged, cleaned, and prepared in Excel.

## Analyses

My primary analysis was conducted in Python, examining potential relationships between median household income and a variety of data points captured in the Vehicle, Snowmobile, and Boat Registrations dataset. Based on my findings between median household income and vehicles per capita in various counties, I wanted to visualize the results on a map instead of a scatter plot. For this, I created chorpeth maps of both variables to examine geographic, rather than linear, trends.

[

[Choropeth Map of Median Income and Vehicles per Capita](https://github.com/DSWeins676/Data-Analysis-Portfolio/blob/main/IncomeDriven/Choropeth_Map_Viz.md)


