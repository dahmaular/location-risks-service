"""
Location Risks API - FastAPI endpoints for location risk assessment
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn

from .location_risk_service import LocationRiskService
from .sea_level_service import SeaLevelService
from .config import Config


class LocationRequest(BaseModel):
    """Request model for location risk analysis."""
    location: str


class LocationResponse(BaseModel):
    """Response model for location risk analysis."""
    location: str
    risk_assessment: str
    success: bool
    error: str = None


class SeaLevelRequest(BaseModel):
    """Request model for sea level analysis."""
    location: str


class SeaLevelResponse(BaseModel):
    """Response model for sea level analysis."""
    location: str
    sea_level_assessment: str
    success: bool
    error: str = None


# Initialize FastAPI app
app = FastAPI(
    title="Location Risk Assessment API",
    description="API for assessing risks associated with specific locations using AI",
    version="1.0.0"
)

# Initialize the services
config = Config()
risk_service = LocationRiskService(config)
sea_level_service = SeaLevelService(config)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Location Risk Assessment API",
        "version": "1.0.0",
        "endpoints": {
            "/analyze": "POST - Analyze location risks",
            "/sea-level": "POST - Analyze sea level and distance to water",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "location-risk-assessment"}


@app.post("/sea-level", response_model=SeaLevelResponse)
async def analyze_sea_level(request: SeaLevelRequest) -> SeaLevelResponse:
    """
    Analyze sea level and distance to water for a given location.

    Args:
        request: SeaLevelRequest containing the location string

    Returns:
        SeaLevelResponse with sea level assessment or error information
    """
    try:
        if not request.location or not request.location.strip():
            raise HTTPException(
                status_code=400,
                detail="Location cannot be empty"
            )

        # Analyze the sea level for the location
        sea_level_assessment = sea_level_service.analyze_location_risk(
            request.location.strip())

        return SeaLevelResponse(
            location=request.location.strip(),
            sea_level_assessment=sea_level_assessment,
            success=True
        )

    except Exception as e:
        error_message = str(e)

        # Handle specific OpenAI API errors
        if "401" in error_message or "invalid_api_key" in error_message:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API configuration error. Please check your API key."
            )
        elif "429" in error_message:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later."
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Error analyzing sea level: {error_message}"
            )


@app.post("/analyze", response_model=LocationResponse)
async def analyze_location(request: LocationRequest) -> LocationResponse:
    """
    Analyze risks for a given location.

    Args:
        request: LocationRequest containing the location string

    Returns:
        LocationResponse with risk assessment or error information
    """
    try:
        if not request.location or not request.location.strip():
            raise HTTPException(
                status_code=400,
                detail="Location cannot be empty"
            )

        # Analyze the location
        risk_assessment = risk_service.analyze_location_risk(
            request.location.strip())

        return LocationResponse(
            location=request.location.strip(),
            risk_assessment=risk_assessment,
            success=True
        )

    except Exception as e:
        error_message = str(e)

        # Handle specific OpenAI API errors
        if "401" in error_message or "invalid_api_key" in error_message:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API configuration error. Please check your API key."
            )
        elif "429" in error_message:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later."
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Error analyzing location: {error_message}"
            )


def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Run the FastAPI server."""
    uvicorn.run(
        "src.api:app",
        host=host,
        port=port,
        reload=reload
    )


if __name__ == "__main__":
    run_server(reload=True)
