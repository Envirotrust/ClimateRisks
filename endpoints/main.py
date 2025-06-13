import uvicorn
from fastapi import FastAPI
from api.route.flood import flood_route
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Flood Risk API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(flood_route, prefix="/api", tags=["Flood Risk"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8082, reload=True)