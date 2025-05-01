import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import recommendations

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Create FastAPI app
app = FastAPI(
    title="Shuts By L'dora",
    description="A luxury fragrance recommendation system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(recommendations.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Shuts By L'dora API. Use /api/welcome to start."}
