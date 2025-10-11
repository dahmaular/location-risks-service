"""
Location Risk Service - Core logic for assessing location-based risks
"""
from openai import OpenAI


class LocationRiskService:
    """Service class for analyzing location risks using OpenAI API."""

    def __init__(self, config):
        """
        Initialize the LocationRiskService.

        Args:
            config: Configuration object containing API keys and settings
        """
        self.config = config
        self.client = OpenAI(api_key=config.get_openai_api_key())

    def analyze_location_risk(self, location: str) -> str:
        """
        Analyze risks for a given location using OpenAI API.

        Args:
            location: The location to analyze (e.g., "San Francisco, CA")

        Returns:
            A string containing the risk assessment
        """
        try:
            prompt = f"""
            Analyze the potential risks for the following location: {location}
            
            Please provide a brief assessment covering:
            1. Floods disaster risks
            2. Fire-related risks
            3. Burglaries and theft risks
            4. Storm-related risks
            5. Collapse risks
            
            Keep the response concise and informative.
            """

            response = self.client.chat.completions.create(
                model="gpt-4.1-2025-04-14",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides location risk assessments."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error analyzing location: {str(e)}"
