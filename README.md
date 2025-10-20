# Location Risks Service

A Python service for assessing location-based risks using OpenAI API. Provides both a command-line interface and a REST API.

## Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   Create a `.env` file and add your configuration:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   
   # API Security Configuration
   API_KEY=your_api_key_here
   VENDOR_ID=your_vendor_id_here
   ```

## Usage

### API Server (Recommended)

Start the FastAPI server:
```bash
python app.py
```

The API will be available at:
- **API Base URL**: `http://localhost:8000`
- **Interactive Documentation**: `http://localhost:8000/docs`
- **Alternative Documentation**: `http://localhost:8000/redoc`

### API Endpoints

#### POST `/analyze`
Analyze location risks.

**Request Body:**
```json
{
  "location": "San Francisco, CA"
}
```

**Response:**
```json
{
  "location": "San Francisco, CA",
  "risk_assessment": "Detailed risk analysis...",
  "success": true,
  "error": null
}
```

#### POST `/sea-level`
Analyze sea level and distance to water for a location.

**Request Body:**
```json
{
  "location": "Venice, Italy"
}
```

**Response:**
```json
{
  "location": "Venice, Italy",
  "sea_level_assessment": "Distance to water and sea level analysis...",
  "success": true,
  "error": null
}
```

#### GET `/health`
Health check endpoint.

#### GET `/`
API information and available endpoints.

### Command Line Interface

Run the basic CLI version:
```bash
python main.py
```

### Testing the API

Use the provided test client:
```bash
python test_client.py
```

Or use curl:

**Location Risk Analysis:**
```bash
curl -X POST "http://localhost:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{"location": "New York, NY"}'
```

**Sea Level Analysis:**
```bash
curl -X POST "http://localhost:8000/sea-level" \
     -H "Content-Type: application/json" \
     -d '{"location": "Amsterdam, Netherlands"}'
```

## Project Structure

- `app.py` - FastAPI server entry point
- `main.py` - CLI application entry point  
- `test_client.py` - API test client
- `src/` - Source code directory
  - `api.py` - FastAPI routes and endpoints
  - `location_risk_service.py` - Core service logic
  - `config.py` - Configuration management
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create this file)

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI services | Yes | - |
| `API_KEY` | API key for client authentication | No | `4590afd6-c4ed-43f1-8f8d` |
| `VENDOR_ID` | Vendor ID for client authentication | No | `c8w3e` |

### Security Configuration

The API uses header-based authentication for protected endpoints:
- **Public endpoints**: `/`, `/health`, `/docs` (no authentication required)
- **Protected endpoints**: `/analyze`, `/sea-level` (require `X-API-Key` and `X-Vendor-ID` headers)

To update the authentication credentials, modify the values in your `.env` file:
```bash
API_KEY=your_new_api_key
VENDOR_ID=your_new_vendor_id
```

## Development

The service uses FastAPI for the web API and OpenAI's GPT model for risk analysis. The API provides structured endpoints for external integration while maintaining the core risk assessment functionality.
