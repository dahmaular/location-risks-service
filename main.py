"""
Location Risks Service - Main Entry Point
"""
from src.location_risk_service import LocationRiskService
from src.config import Config


def main():
    """Main function to run the location risk service."""
    config = Config()
    service = LocationRiskService(config)

    # # Example usage
    # location = "San Francisco, CA"
    # print(f"Analyzing risks for: {location}")

    # result = service.analyze_location_risk(location)
    # print(f"\nRisk Assessment:\n{result}")


if __name__ == "__main__":
    main()
