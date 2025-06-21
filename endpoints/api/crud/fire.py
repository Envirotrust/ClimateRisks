"""
Author: Ajeyomi Adedoyin Samuel
Email: adedoyinsmuel25@gmail.com
Title: Fire Risk Intersect Checker

Description:
------------
This script reads a fire risk dataset stored in Zarr format on AWS S3, loads it using xarray,
and checks if a given geographic coordinate intersects any fire risk layers.
It returns the fire risk values at that location.


Dependencies:
-------------
- xarray
- zarr  
- dask
- s3fs
- typing

Function:
---------
get_fire_risk_information(bucket, key, longitude, latitude)
    Takes a geographic coordinate and retrieves the corresponding fire risk values
    from a Zarr file stored on S3.

get_fire_weather_risk_info(longitude, latitude, bucket=None, key=None, local_path=None)
    Retrieves fire weather risk information for a specific geographic point.

Usage:
------
- Ensure the `AWS_ACCESS_KEY` and `AWS_SECRET_KEY` are set in your environment.
- Provide the correct S3 bucket and Zarr key.
- Call `get_fire_risk_information()` with the desired longitude and latitude.
- Optionally, you can specify a local path to a Zarr file instead of S3.
- Call `get_fire_weather_risk_info()` to get fire weather risk data for a point.
- Ensure the Zarr file is structured correctly with the necessary variables.

Note:
-----
- The Zarr file must have longitude (`x`) and latitude (`y`) as coordinates.
- The function uses nearest neighbor interpolation to find the closest grid cell to the provided coordinates.
- The returned dictionary includes the longitude, latitude, and fire risk variables.
- The function returns a dictionary with the longitude, latitude, and all fire risk variables at that point.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


import xarray as xr
from typing import Optional
from core.config import FIRE_WEATHER_RISK
from .utils.utils import (validate_coordinates, validate_bucket_and_key, 
                        validate_credentials, validate_european_coordinates)

from dotenv import load_dotenv

load_dotenv()


# Load AWS credentials from environment variables
ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
SECRET_KEY = os.getenv("AWS_SECRET_KEY")
BUCKET = os.getenv("S3_BUCKET")
KEY = os.getenv("S3_FIRE_RISK_KEY")

def get_fire_risk_information(
                            longitude:float,
                            latitude:float,
                            bucket:str=BUCKET,
                            key:str=KEY,
                              ) -> dict:
    """Retrieve fire risk information for a specific geographic point from a Zarr dataset on S3."""

    # Validate inputs
    longitude, latitude = validate_coordinates(longitude, latitude)
    longitude, latitude = validate_european_coordinates(longitude, latitude)
    bucket, key = validate_bucket_and_key(bucket, key)
    validate_credentials(ACCESS_KEY, SECRET_KEY)
     
    
    zarr_path = f's3://{bucket}/{key}'
    
    try:     
        # Open Zarr via s3fs
        fire_datasets = xr.open_zarr(zarr_path, consolidated=True, storage_options={'anon': False, 'key': ACCESS_KEY, 'secret': SECRET_KEY})

        # Select nearest grid cell to the given coordinate
        point_data = fire_datasets.sel(x=longitude, y=latitude, method='nearest')

        # Convert all data variables to key-value pairs (rounded)
        point_dict = {
            str(var): round(float(point_data[var].values), 2)
            for var in point_data.data_vars
        }

        point_dict["longitude"] = round(float(point_data.coords["x"].values), 6)
        point_dict["latitude"] = round(float(point_data.coords["y"].values), 6)


        results = {
            "High_risk": point_dict.get('High risk (aggr. wildfire risk)'),
            "Intermediate_risk": point_dict.get( 'Intermediate risk (aggr. wildfire risk)'),
            "Low_risk": point_dict.get('Low risk (aggr. wildfire risk)'),
            "Potential_burnable_land_proportion": point_dict.get('Potential burnable land proportion'),
            "Wildland_Urban_Interface": point_dict.get('Wildland-Urban Interface (WUI)'),
            "longitude": point_dict["longitude"],
            "latitude": point_dict["latitude"]
        }

        return {"fire_risk_data": results}
    
    except KeyError as e:
        raise KeyError(f"KeyError: {str(e)} — Check if the Zarr file contains the required variables.")

    except ValueError as e:
        raise ValueError(f"ValueError: {str(e)} — Check if the coordinates are within dataset bounds.")

    except Exception as e:
        raise RuntimeError(f"Unexpected error while accessing Zarr data: {str(e)}")



def get_fire_weather_risk_information(
        longitude: float,
        latitude: float,
        bucket: Optional[str] = None,
        key: Optional[str] = None,
        local_path: Optional[str] = FIRE_WEATHER_RISK
    ) -> dict:
    """Retrieve fire weather risk information for a specific geographic point."""

    # Validate inputs
    longitude, latitude = validate_coordinates(longitude, latitude)
    longitude, latitude = validate_european_coordinates(longitude, latitude)

    if bucket is not None:
        bucket, key = validate_bucket_and_key(bucket, key)
        validate_credentials(ACCESS_KEY, SECRET_KEY)

    try:
        if bucket and key:
            zarr_path = f's3://{bucket}/{key}'
            fire_risk = xr.open_zarr(zarr_path, consolidated=True, storage_options={'anon': False, 'key': ACCESS_KEY, 'secret': SECRET_KEY})
        else:
            fire_risk = xr.open_zarr(local_path, decode_timedelta=False)

    except FileNotFoundError:
        raise FileNotFoundError(f"Zarr file not found at {local_path} or in S3 bucket {bucket} with key {key}.")
    
    try:
        # Detect latitude and longitude variable names
        lat_name = None
        lon_name = None
        for possible_lat in ['lat', 'latitude', 'y']:
            if possible_lat in fire_risk.coords:
                lat_name = possible_lat
                break
        for possible_lon in ['lon', 'longitude', 'x']:
            if possible_lon in fire_risk.coords:
                lon_name = possible_lon
                break
        if lat_name is None or lon_name is None:
            raise KeyError("Could not find latitude or longitude coordinate in the dataset.")

        # Compute squared distance
        distance = (fire_risk[lat_name] - latitude)**2 + (fire_risk[lon_name] - longitude)**2

        # Get the index of the closest point
        closest_index = distance.argmin().compute().item()

        point_data = fire_risk.isel(point=closest_index).to_dataframe().reset_index()

        vars_of_interest = ['year', 'days_moderate_fire_danger', 'days_high_fire_danger', 'days_very_high_fire_danger']
        available_vars = [var for var in vars_of_interest if var in point_data.columns]
        if not available_vars or 'year' not in available_vars:
            raise KeyError(f"None of the required variables {vars_of_interest} found in the dataset columns: {point_data.columns.tolist()}")
        point_data = point_data[available_vars].astype(int).groupby('year').sum().reset_index()

        # Add constant latitude and longitude columns
        point_data['latitude'] = latitude
        point_data['longitude'] = longitude

        result = point_data.to_dict(orient='records')

        return {"fire_weather_risk_data": result}
    
    except KeyError as e:
        raise KeyError(f"KeyError: {str(e)} — Check if the Zarr file contains the required variables or coordinate names (lat/lon).")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while accessing Zarr data: {str(e)}")

