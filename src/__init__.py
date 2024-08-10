from fastapi import FastAPI
from src.pokemon_simulator.routes import router

version = "v1"

app = FastAPI(
    version = version
)

app.include_router(router, prefix="")