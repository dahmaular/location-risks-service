"""
Vercel serverless function entry point - Web API compatible
"""
import sys
import os
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Add the parent directory to Python path so we can import from src
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


class handler(BaseHTTPRequestHandler):
    """Vercel-compatible HTTP handler class"""

    def do_GET(self):
        """Handle GET requests"""
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path

            if path == '/' or path == '':
                response_data = {
                    "message": "Location Risk Assessment API",
                    "version": "1.0.0",
                    "endpoints": {
                        "/analyze": "POST - Analyze location risks",
                        "/sea-level": "POST - Analyze sea level",
                        "/health": "GET - Health check"
                    }
                }
                self._send_response(200, response_data)

            elif path == '/health':
                response_data = {"status": "healthy",
                                 "service": "location-risk-assessment"}
                self._send_response(200, response_data)

            else:
                self._send_response(404, {"error": "Route not found"})

        except Exception as e:
            self._send_response(500, {"error": f"Server error: {str(e)}"})

    def do_POST(self):
        """Handle POST requests"""
        try:
            # Import services here to avoid module-level import issues
            from src.location_risk_service import LocationRiskService
            from src.sea_level_service import SeaLevelService
            from src.config import Config

            # Initialize services
            config = Config()
            risk_service = LocationRiskService(config)
            sea_level_service = SeaLevelService(config)

            parsed_path = urlparse(self.path)
            path = parsed_path.path

            # Parse request body
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length).decode('utf-8')
                try:
                    body_data = json.loads(body)
                except json.JSONDecodeError:
                    self._send_response(
                        400, {"error": "Invalid JSON in request body"})
                    return
            else:
                body_data = {}

            location = body_data.get('location', '').strip()
            if not location:
                self._send_response(400, {"error": "Location cannot be empty"})
                return

            if path == '/analyze':
                try:
                    risk_assessment = risk_service.analyze_location_risk(
                        location)
                    response_data = {
                        "location": location,
                        "risk_assessment": risk_assessment,
                        "success": True,
                        "error": None
                    }
                    self._send_response(200, response_data)
                except Exception as e:
                    self._handle_service_error(e, location, "risk_assessment")

            elif path == '/sea-level':
                try:
                    sea_level_assessment = sea_level_service.analyze_location_risk(
                        location)
                    response_data = {
                        "location": location,
                        "sea_level_assessment": sea_level_assessment,
                        "success": True,
                        "error": None
                    }
                    self._send_response(200, response_data)
                except Exception as e:
                    self._handle_service_error(
                        e, location, "sea_level_assessment")

            else:
                self._send_response(404, {"error": "Route not found"})

        except ImportError as e:
            self._send_response(500, {"error": f"Import error: {str(e)}"})
        except Exception as e:
            self._send_response(500, {"error": f"Server error: {str(e)}"})

    def _handle_service_error(self, error, location, assessment_type):
        """Handle service-specific errors"""
        error_message = str(error)
        if "401" in error_message or "invalid_api_key" in error_message:
            status_code = 500
            error_detail = "OpenAI API configuration error. Please check your API key."
        elif "429" in error_message:
            status_code = 429
            error_detail = "Rate limit exceeded. Please try again later."
        else:
            status_code = 500
            error_detail = f"Error analyzing location: {error_message}"

        response_data = {
            "location": location,
            assessment_type: None,
            "success": False,
            "error": error_detail
        }
        self._send_response(status_code, response_data)

    def _send_response(self, status_code, data):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        response_json = json.dumps(data, indent=2)
        self.wfile.write(response_json.encode('utf-8'))

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
