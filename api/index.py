"""
Vercel serverless function entry point
"""
import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum

# Add the parent directory to Python path so we can import from src
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    from src.location_risk_service import LocationRiskService
    from src.sea_level_service import SeaLevelService
    from src.config import Config

    # Initialize FastAPI app
    app = FastAPI(
        title="Location Risk Assessment API",
        description="API for assessing risks associated with specific locations using AI",
        version="1.0.0"
    )

    # Initialize services
    config = Config()
    risk_service = LocationRiskService(config)
    sea_level_service = SeaLevelService(config)

    # Request/Response models
    class LocationRequest(BaseModel):
        location: str

    class LocationResponse(BaseModel):
        location: str
        risk_assessment: str
        success: bool
        error: str = None

    class SeaLevelRequest(BaseModel):
        location: str

    class SeaLevelResponse(BaseModel):
        location: str
        sea_level_assessment: str
        success: bool
        error: str = None

    # Routes
    @app.get("/")
    async def root():
        return {
            "message": "Location Risk Assessment API",
            "version": "1.0.0",
            "endpoints": {
                "/analyze": "POST - Analyze location risks",
                "/sea-level": "POST - Analyze sea level",
                "/health": "GET - Health check"
            }
        }

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "location-risk-assessment"}

    @app.post("/analyze", response_model=LocationResponse)
    async def analyze_location(request: LocationRequest) -> LocationResponse:
        try:
            if not request.location or not request.location.strip():
                raise HTTPException(
                    status_code=400, detail="Location cannot be empty")

            risk_assessment = risk_service.analyze_location_risk(
                request.location.strip())

            return LocationResponse(
                location=request.location.strip(),
                risk_assessment=risk_assessment,
                success=True
            )
        except Exception as e:
            error_message = str(e)
            if "401" in error_message or "invalid_api_key" in error_message:
                raise HTTPException(
                    status_code=500, detail="OpenAI API configuration error. Please check your API key.")
            elif "429" in error_message:
                raise HTTPException(
                    status_code=429, detail="Rate limit exceeded. Please try again later.")
            else:
                raise HTTPException(
                    status_code=500, detail=f"Error analyzing location: {error_message}")

    @app.post("/sea-level", response_model=SeaLevelResponse)
    async def analyze_sea_level(request: SeaLevelRequest) -> SeaLevelResponse:
        try:
            if not request.location or not request.location.strip():
                raise HTTPException(
                    status_code=400, detail="Location cannot be empty")

            sea_level_assessment = sea_level_service.analyze_location_risk(
                request.location.strip())

            return SeaLevelResponse(
                location=request.location.strip(),
                sea_level_assessment=sea_level_assessment,
                success=True
            )
        except Exception as e:
            error_message = str(e)
            if "401" in error_message or "invalid_api_key" in error_message:
                raise HTTPException(
                    status_code=500, detail="OpenAI API configuration error. Please check your API key.")
            elif "429" in error_message:
                raise HTTPException(
                    status_code=429, detail="Rate limit exceeded. Please try again later.")
            else:
                raise HTTPException(
                    status_code=500, detail=f"Error analyzing sea level: {error_message}")

    # Create the handler for Vercel
    handler = Mangum(app)

except ImportError as e:
    print(f"Import error: {e}")

    # Fallback FastAPI app
    app = FastAPI(title="Error", description="Import Error")

    @app.get("/")
    async def error_root():
        return {"error": f"Import error: {str(e)}"}

    handler = Mangum(app)
