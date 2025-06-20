from fastapi import APIRouter, HTTPException
from api.crud.fire import get_fire_risk_information
from schema.fire import FireRiskDataResponse

import sys
import os
sys.path.append(os.path.dirname(__file__))


fire_route = APIRouter()

@fire_route.get("/fire-risk",
         response_model=FireRiskDataResponse,
         status_code=200,
         tags=["Fire Risk"],
         description="Check the fire risk for a particular location")
async def get_fire_risk_info(longitude: float, latitude: float) -> FireRiskDataResponse:
    """Check the fire risk for the given latitude and longitude and return info as Dict"""
    try:
        data = get_fire_risk_information(longitude, latitude)
        if not data:
            raise HTTPException(
                status_code=404,
                detail=f"No data available for ({latitude}, {longitude})."
            )
        return data
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")
