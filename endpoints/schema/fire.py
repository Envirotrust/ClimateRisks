from pydantic import BaseModel
from typing import Dict

class FireRiskData(BaseModel):
    High_risk: float
    Intermediate_risk: float
    Low_risk: float
    Potential_burnable_land_proportion: float
    Wildland_Urban_Interface: float
    longitude: float
    latitude: float

class FireRiskDataResponse(BaseModel):
    fire_risk_data: FireRiskData

    class Config:
        json_schema_extra = {
            "example": {
                "fire_risk_data": {
                    "High_risk": 0.75,
                    "Intermediate_risk": 0.15,
                    "Low_risk": 0.1,
                    "Potential_burnable_land_proportion": 0.5,
                    "Wildland_Urban_Interface": 0.2,
                    "longitude": 12.34,
                    "latitude": 56.78
                }
            }
        }


class FireRiskWeatherData(BaseModel):
    year: int
    days_moderate_fire_danger: int
    days_high_fire_danger: int
    days_very_high_fire_danger: int
    longitude: float
    latitude: float

class FireRiskWeatherMultiYearResponse(BaseModel):
    fire_weather_risk_data: Dict[int, FireRiskWeatherData]

    class Config:
        json_schema_extra = {
            "example": {
                "fire_weather_risk_data": {
                    "2005": {
                        "year": 2005,
                        "days_moderate_fire_danger": 180,
                        "days_high_fire_danger": 90,
                        "days_very_high_fire_danger": 45,
                        "longitude": 12.34,
                        "latitude": 56.78
                    },
                    "2006": {
                        "year": 2006,
                        "days_moderate_fire_danger": 216,
                        "days_high_fire_danger": 108,
                        "days_very_high_fire_danger": 52,
                        "longitude": 12.34,
                        "latitude": 56.78
                    }
                }
            }
        }