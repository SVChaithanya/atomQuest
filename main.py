from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from db import Base, engine
from router import router

app = FastAPI(title="Goal Tracking Portal")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# IMPORTANT: API first
app.include_router(router, prefix="/api")

# IMPORTANT: STATIC LAST (this fixes your issue)
app.mount("/ui", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/")
def home():
    return {"message": "Goal Tracking Portal Running"}