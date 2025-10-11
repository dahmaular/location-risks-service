"""
Vercel serverless function entry point
"""
from src.api import app
import sys
import os

# Add the parent directory to Python path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Export the FastAPI app for Vercel
handler = app
