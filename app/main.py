# from fastapi import FastAPI
# from app.routes import explain, health

# app = FastAPI(title="SQL Explainer API")

# app.include_router(health.router)
# app.include_router(explain.router)

# @app.get("/")
# def root():
#     return {"status": "SQL Explainer backend running"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import explain, health

app = FastAPI(title="SQL Explainer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.1.2:3000",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(explain.router)
