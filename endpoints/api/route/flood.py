from fastapi import APIRouter, HTTPException
from api.crud.flood import get_flood_information
from schema.flood import FloodDataResponse

import sys
import os
sys.path.append(os.path.dirname(__file__))


flood_route = APIRouter()

@flood_route.get("/flood-risk",
         response_model=FloodDataResponse,
         status_code=200,
         tags=["Flood Risk"],
         description="Check if a particular location is flooded or not")
async def get_flood_info(longitude: float, latitude: float) -> FloodDataResponse:
    """Check if the latitudes and longitudes intersect with flood areas and return info as JSON"""
    try:
        data = get_flood_information(longitude, latitude)
        if not data:
            raise HTTPException(
                status_code=404,
                detail=f"No flood risk data found for location ({latitude}, {longitude})."
            )
        return data
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")
