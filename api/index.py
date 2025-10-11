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
                        "/health": "GET - Health check",
                        "/docs": "GET - API Documentation"
                    }
                }
                self._send_response(200, response_data)

            elif path == '/health':
                response_data = {"status": "healthy",
                                 "service": "location-risk-assessment"}
                self._send_response(200, response_data)

            elif path == '/docs':
                self._send_docs_page()

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

    def _send_docs_page(self):
        """Send HTML documentation page"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Location Risk Assessment API - Documentation</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; line-height: 1.6; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 30px; }
        .endpoint { background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 5px; margin: 20px 0; padding: 20px; }
        .method { display: inline-block; padding: 4px 8px; border-radius: 3px; font-weight: bold; color: white; margin-right: 10px; }
        .get { background: #28a745; }
        .post { background: #007bff; }
        .path { font-family: monospace; font-size: 18px; font-weight: bold; }
        .example { background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 5px; margin: 10px 0; overflow-x: auto; }
        .response { background: #1a202c; color: #68d391; padding: 15px; border-radius: 5px; margin: 10px 0; overflow-x: auto; }
        pre { margin: 0; white-space: pre-wrap; }
        .description { margin: 10px 0; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌍 Location Risk Assessment API</h1>
        <p>AI-powered location risk assessment and sea level analysis</p>
        <p><strong>Version:</strong> 1.0.0</p>
    </div>

    <div class="endpoint">
        <span class="method get">GET</span>
        <span class="path">/</span>
        <div class="description">Get API information and available endpoints</div>
        <div class="example">
<pre>curl https://your-domain.vercel.app/</pre>
        </div>
    </div>

    <div class="endpoint">
        <span class="method get">GET</span>
        <span class="path">/health</span>
        <div class="description">Health check endpoint</div>
        <div class="example">
<pre>curl https://your-domain.vercel.app/health</pre>
        </div>
        <div class="response">
<pre>{
  "status": "healthy",
  "service": "location-risk-assessment"
}</pre>
        </div>
    </div>

    <div class="endpoint">
        <span class="method post">POST</span>
        <span class="path">/analyze</span>
        <div class="description">Analyze location risks using AI</div>
        <div class="example">
<pre>curl -X POST https://your-domain.vercel.app/analyze \\
  -H "Content-Type: application/json" \\
  -d '{
    "location": "San Francisco, CA"
  }'</pre>
        </div>
        <div class="response">
<pre>{
  "location": "San Francisco, CA",
  "risk_assessment": "Detailed AI-generated risk analysis...",
  "success": true,
  "error": null
}</pre>
        </div>
    </div>

    <div class="endpoint">
        <span class="method post">POST</span>
        <span class="path">/sea-level</span>
        <div class="description">Analyze sea level and water distance for a location</div>
        <div class="example">
<pre>curl -X POST https://your-domain.vercel.app/sea-level \\
  -H "Content-Type: application/json" \\
  -d '{
    "location": "Miami, FL"
  }'</pre>
        </div>
        <div class="response">
<pre>{
  "location": "Miami, FL",
  "sea_level_assessment": "1. Distance to water assessment...\\n2. Distance to sea level assessment...\\n3. Distance to sea level: 0 km\\n4. Distance to water: 1.2 km",
  "success": true,
  "error": null
}</pre>
        </div>
    </div>

    <div class="endpoint">
        <h3>📋 Request/Response Format</h3>
        <h4>Request Body (for POST endpoints):</h4>
        <div class="example">
<pre>{
  "location": "string (required) - Location to analyze (e.g., 'Tokyo, Japan')"
}</pre>
        </div>
        
        <h4>Success Response:</h4>
        <div class="response">
<pre>{
  "location": "string - The analyzed location",
  "risk_assessment": "string - AI-generated risk analysis (for /analyze)",
  "sea_level_assessment": "string - Sea level analysis (for /sea-level)",
  "success": true,
  "error": null
}</pre>
        </div>
        
        <h4>Error Response:</h4>
        <div class="response">
<pre>{
  "location": "string - The requested location",
  "risk_assessment": null,
  "success": false,
  "error": "string - Error description"
}</pre>
        </div>
    </div>

    <div class="endpoint">
        <h3>🔧 Environment Setup</h3>
        <p>This API requires an OpenAI API key to function. Make sure the <code>OPENAI_API_KEY</code> environment variable is properly configured.</p>
    </div>

    <div class="endpoint">
        <h3>🌐 CORS Support</h3>
        <p>This API supports Cross-Origin Resource Sharing (CORS) and can be called from web browsers.</p>
    </div>

    <footer style="margin-top: 50px; text-align: center; color: #666; border-top: 1px solid #eee; padding-top: 20px;">
        <p>Location Risk Assessment API • Built with Python • Powered by OpenAI</p>
    </footer>
</body>
</html>
"""

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
