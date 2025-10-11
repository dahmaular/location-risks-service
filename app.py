"""
Location Risks Service - Vercel Serverless Function Entry Point
"""
import uvicorn
from src.api import app

# Export the FastAPI app for Vercel
handler = app


def main():
    """Main function to run the FastAPI server locally."""
    print("Starting Location Risk Assessment API server...")
    print("API Documentation will be available at: http://localhost:8000/docs")
    print("API will be accessible at: http://localhost:8000")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main()
