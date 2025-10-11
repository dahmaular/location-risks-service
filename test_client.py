"""
Test client for Location Risk Assessment API
"""
import requests
import json


def test_api(base_url: str = "http://localhost:8000"):
    """Test the Location Risk Assessment API."""

    print("Testing Location Risk Assessment API")
    print(f"Base URL: {base_url}")
    print("-" * 50)

    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except requests.exceptions.ConnectionError:
        print("❌ API server is not running. Please start it first with: python app.py")
        return

    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"Root Endpoint: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
    except Exception as e:
        print(f"Error testing root endpoint: {e}")

    # Test location analysis
    print("🔍 Testing Location Risk Analysis...")
    test_locations = [
        "San Francisco, CA",
        "Tokyo, Japan",
        "London, UK",
        "Miami, FL"
    ]

    for location in test_locations:
        try:
            payload = {"location": location}
            response = requests.post(f"{base_url}/analyze", json=payload)

            print(f"Analyzing: {location}")
            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success: {result['success']}")
                print(
                    f"Risk Assessment Preview: {result['risk_assessment'][:100]}...")
            else:
                print(f"❌ Error: {response.json()}")

            print("-" * 30)

        except Exception as e:
            print(f"Error analyzing {location}: {e}")
            print("-" * 30)

    # Test sea level analysis
    print("\n🌊 Testing Sea Level Analysis...")
    sea_level_locations = [
        "Venice, Italy",
        "Amsterdam, Netherlands",
        "New Orleans, Louisiana",
        "Denver, Colorado"
    ]

    for location in sea_level_locations:
        try:
            payload = {"location": location}
            response = requests.post(f"{base_url}/sea-level", json=payload)

            print(f"Sea Level Analysis: {location}")
            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success: {result['success']}")
                print(
                    f"Sea Level Assessment Preview: {result['sea_level_assessment'][:100]}...")
            else:
                print(f"❌ Error: {response.json()}")

            print("-" * 30)

        except Exception as e:
            print(f"Error analyzing sea level for {location}: {e}")
            print("-" * 30)


if __name__ == "__main__":
    test_api()
