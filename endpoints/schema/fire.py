from pydantic import BaseModel

class FireRiskData(BaseModel):
    High_risk:float
    Low_risk: float
    Intermediate_risk: float
    Potential_burnable_land_proportion: float
    Wildland_Urban_Interface: float
    longitude: float
    latitude: float
    
class FireRiskDataResponse(BaseModel):

    fire_risk_data: FireRiskData

    class Config:
        schema_extra = {
            "example": {
                "fire_risk_data": {
                    "High_risk": 0.75,
                    "Low_risk": 0.1,
                    "Intermediate_risk": 0.15,
                    "Potential_burnable_land_proportion": 0.5,
                    "Wildland_Urban_Interface": 0.2,
                    "longitude": 12.34,
                    "latitude": 56.78
                }
            }
        }