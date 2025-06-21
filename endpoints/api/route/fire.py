from fastapi import APIRouter, HTTPException, Query
from api.crud.fire import get_fire_risk_information, get_fire_weather_risk_information
from schema.fire import FireRiskDataResponse, FireRiskWeatherData, FireRiskWeatherMultiYearResponse

fire_route = APIRouter()

@fire_route.get("/fire-risk",
    response_model=FireRiskDataResponse,
    status_code=200,
    tags=["Fire Risk"],
    description="Check the fire risk for a particular location"
)
async def get_fire_risk_info(
    longitude: float = Query(..., gt=-180, lt=180, description="Longitude must be between -180 and 180."),
    latitude: float = Query(..., gt=-90, lt=90, description="Latitude must be between -90 and 90.")
) -> FireRiskDataResponse:
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


@fire_route.get("/fire-weather-risk",
    response_model=FireRiskWeatherMultiYearResponse,
    status_code=200,
    tags=["Fire Risk"],
    description="Check the fire weather risk for all available years for a particular location"
)
async def get_fire_weather_risk_info(
    longitude: float = Query(..., gt=-180, lt=180, description="Longitude must be between -180 and 180."),
    latitude: float = Query(..., gt=-90, lt=90, description="Latitude must be between -90 and 90."),
) -> FireRiskWeatherMultiYearResponse:
    try:
        raw_data = get_fire_weather_risk_information(longitude, latitude)

        # Extract list of records
        records = raw_data.get("fire_weather_risk_data", [])
        if not records:
            raise HTTPException(status_code=404, detail=f"No data available for ({latitude}, {longitude}).")

        formatted_data = {}
        for record in records:
            year = record.get("year")
            if year is None:
                continue 

            # Create FireRiskWeatherData instance
            data_obj = FireRiskWeatherData(**record)
            formatted_data[year] = data_obj

        if not formatted_data:
            raise HTTPException(status_code=404, detail=f"No valid fire weather risk data found for ({latitude}, {longitude}).")

        return FireRiskWeatherMultiYearResponse(fire_weather_risk_data=formatted_data)

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
