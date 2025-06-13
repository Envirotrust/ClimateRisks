from pydantic import BaseModel

class FloodDataResponse(BaseModel):
    longitude:float
    latitude:float
    flood_zone: bool