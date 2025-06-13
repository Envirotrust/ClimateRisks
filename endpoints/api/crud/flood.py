"""
Author: Ajeyomi Adedoyin Samuel
Email: adedoyinsmuel25@gmail.com
Title: Flood Risk Intersect Checker

Description:
------------
This script Loads flood risk polygon data(parquet file), loads it using duckdb, 
and check if the coordinate point(s) intersect with the flood-prone areas.

IT accepts Geoparquet with lon and lat of a location and applies spatial 
analysis to determine whether input geographic points fall within any of the designated flood zones.

Modules:
--------
- duckdb
- typing
- shapely

Functions:
---------
get_flood_information(bucket, key, longitude, latitude)
    Get a geographical coordinates as input and  checks if they intersect with flood zones,
    and returns the results as JSON.

Usage:
------
- Ensure you put the correct path to your parqet file
- Call `get_flood_information()` with either single or list of `longitude` and `latitude` values.

Note:
-----
- This script assumes that the geospatial data is readable by duckdb and contains a geometry column.
"""



import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from .utils.duckdb import setup_spatial_extensions
from .utils.utils import validate_coordinates
import duckdb
import json
from shapely.geometry import Point
from core.config import FLOOD_DATA



def get_flood_information(
    point_lon: float,
    point_lat: float,
    parquet_path:str=FLOOD_DATA,
    buffer_degrees: float = 0.00001  # ~0.1m buffer for pre-filtering
) -> json:
    """Check if a coordinate intersect with flood zones"""  
    
    # validate the input coordinates
    validate_coordinates(point_lon, point_lat)

    # Setup spatial extensions
    setup_spatial_extensions()
    
    # Create point and bounding box
    point_wkt = Point(point_lon, point_lat).wkt
    
    # Bounding box for pre-filtering
    bbox_min_lon = point_lon - buffer_degrees
    bbox_max_lon = point_lon + buffer_degrees  
    bbox_min_lat = point_lat - buffer_degrees
    bbox_max_lat = point_lat + buffer_degrees
    
    print(f"Checking intersection for: {point_wkt}")
    print(f"Using bounding box filter: [{bbox_min_lon:.6f}, {bbox_min_lat:.6f}, {bbox_max_lon:.6f}, {bbox_max_lat:.6f}]")
    
    try:
        print("Running optimized spatial query...")
        result = duckdb.sql(f"""
                    SELECT 1
                  FROM (
                      SELECT geometry
                      FROM read_parquet('{parquet_path}')
                  )
                WHERE 
                    -- Fast bounding box pre-filter using geometry bounds
                    ST_XMin(geometry) <= {bbox_max_lon}
                    AND ST_XMax(geometry) >= {bbox_min_lon}
                    AND ST_YMin(geometry) <= {bbox_max_lat}
                    AND ST_YMax(geometry) >= {bbox_min_lat}
                    -- Perform expensive intersection
                    AND ST_Intersects(geometry, ST_GeomFromText('{point_wkt}'))
                LIMIT 1
            """).fetchone()
        
        intersects = result is not None
         
        result = {
                "longitude": point_lon,
                "latitude": point_lat,
                "flood_zone": intersects
            }
        
        return result
    
    except Exception as e:
        raise RuntimeError(f"{e.__class__.__name__}: {str(e)}")


# if __name__ == "__main__":
#     start_time = time.time()

#     point_lon=12.772144
#     point_lat=45.562546

    
#     result = get_flood_information(
#             point_lon=point_lon,
#             point_lat=point_lat,
#             parquet_path=FLOOD_DATA)
    
#     elapsed = time.time() - start_time
#     print(f"Total time taken: {elapsed:.2f}s - Result: {result}")
    