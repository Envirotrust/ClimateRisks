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

Usage:
------
- Ensure the `AWS_ACCESS_KEY` and `AWS_SECRET_KEY` are set in your environment.
- Provide the correct S3 bucket and Zarr key.
- Call `get_fire_risk_information()` with bucket, key, longitude, and latitude.

Note:
-----
- The Zarr file must have longitude (`x`) and latitude (`y`) as coordinates.
- The function returns a dictionary with the longitude, latitude, and all fire risk variables at that point.
"""

import os
import sys
import xarray as xr
import zarr
import dask
import s3fs
from utils.utils import (validate_coordinates, validate_bucket_and_key, 
                        validate_credentials, validate_european_coordinates)

from dotenv import load_dotenv

load_dotenv()


# Load AWS credentials from environment variables
ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
SECRET_KEY = os.getenv("AWS_SECRET_KEY")
BUKCET = os.getenv("s3_BUCKET")
KEY = os.getenv("s3_FIRE_RISK_KEY")

def get_fire_risk_information(
                            longitude:float,
                            latitude:float,
                            bucket:str=BUKCET,
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

        return results
    
    except KeyError as e:
        raise KeyError(f"KeyError: {str(e)} — Check if the Zarr file contains the required variables.")

    except ValueError as e:
        raise ValueError(f"ValueError: {str(e)} — Check if the coordinates are within dataset bounds.")

    except Exception as e:
        raise RuntimeError(f"Unexpected error while accessing Zarr data: {str(e)}")


if __name__ == "__main__":
    bucket = 'envirotrust-staging'
    key = 'fire_risks/fire_risks_variables'
    longitude = 12.772144
    latitude = 45.562546

    fire_risk_info = get_fire_risk_information(longitude, latitude,bucket, key)
    print(fire_risk_info)
