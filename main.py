from contextlib import asynccontextmanager
from fastapi import FastAPI
import os

from app.api.router import router
from app.core.db import Database

@asynccontextmanager
async def lifespan(app: FastAPI):
    api_prefix = os.getenv("API_PREFIX", "")

    await Database.connect(os.getenv("MONGO_URI"), os.getenv("DB_NAME"))
    print("Mongo client connected and beanie initialised successfully")

    app.include_router(router, prefix=api_prefix)

    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return "Hello"