"""
Vercel serverless function entry point - Simple HTTP handler approach
"""
import sys
import os
import json
from urllib.parse import parse_qs

# Add the parent directory to Python path so we can import from src
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


def handler(request):
    """Simple HTTP handler for Vercel without FastAPI/Mangum complications"""
    try:
        # Import here to avoid module-level import issues
        from src.location_risk_service import LocationRiskService
        from src.sea_level_service import SeaLevelService
        from src.config import Config

        # Initialize services
        config = Config()
        risk_service = LocationRiskService(config)
        sea_level_service = SeaLevelService(config)

        # Get request method and path
        method = request.get('httpMethod', 'GET')
        path = request.get('path', '/')

        # Handle different routes
        if method == 'GET':
            if path == '/' or path == '':
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        "message": "Location Risk Assessment API",
                        "version": "1.0.0",
                        "endpoints": {
                            "/analyze": "POST - Analyze location risks",
                            "/sea-level": "POST - Analyze sea level",
                            "/health": "GET - Health check"
                        }
                    })
                }
            elif path == '/health':
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({"status": "healthy", "service": "location-risk-assessment"})
                }

        elif method == 'POST':
            # Parse request body
            body = request.get('body', '{}')
            if isinstance(body, str):
                try:
                    body_data = json.loads(body)
                except json.JSONDecodeError:
                    return {
                        'statusCode': 400,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({"error": "Invalid JSON in request body"})
                    }
            else:
                body_data = body

            location = body_data.get('location', '').strip()
            if not location:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({"error": "Location cannot be empty"})
                }

            if path == '/analyze':
                try:
                    risk_assessment = risk_service.analyze_location_risk(
                        location)
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({
                            "location": location,
                            "risk_assessment": risk_assessment,
                            "success": True,
                            "error": None
                        })
                    }
                except Exception as e:
                    error_message = str(e)
                    if "401" in error_message or "invalid_api_key" in error_message:
                        status_code = 500
                        error_detail = "OpenAI API configuration error. Please check your API key."
                    elif "429" in error_message:
                        status_code = 429
                        error_detail = "Rate limit exceeded. Please try again later."
                    else:
                        status_code = 500
                        error_detail = f"Error analyzing location: {error_message}"

                    return {
                        'statusCode': status_code,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({
                            "location": location,
                            "risk_assessment": None,
                            "success": False,
                            "error": error_detail
                        })
                    }

            elif path == '/sea-level':
                try:
                    sea_level_assessment = sea_level_service.analyze_location_risk(
                        location)
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({
                            "location": location,
                            "sea_level_assessment": sea_level_assessment,
                            "success": True,
                            "error": None
                        })
                    }
                except Exception as e:
                    error_message = str(e)
                    if "401" in error_message or "invalid_api_key" in error_message:
                        status_code = 500
                        error_detail = "OpenAI API configuration error. Please check your API key."
                    elif "429" in error_message:
                        status_code = 429
                        error_detail = "Rate limit exceeded. Please try again later."
                    else:
                        status_code = 500
                        error_detail = f"Error analyzing sea level: {error_message}"

                    return {
                        'statusCode': status_code,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({
                            "location": location,
                            "sea_level_assessment": None,
                            "success": False,
                            "error": error_detail
                        })
                    }

        # Route not found
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"error": "Route not found"})
        }

    except ImportError as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"error": f"Import error: {str(e)}"})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"error": f"Server error: {str(e)}"})
        }
