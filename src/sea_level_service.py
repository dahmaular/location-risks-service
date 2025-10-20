from openai import OpenAI


class SeaLevelService:
    """Service class for analyzing sea level risks using OpenAI API."""

    def __init__(self, config):
        """
        Initialize the SeaLevelService.

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
            Calculate the distance from sea level for the following location: {location}
            
            Please provide a response that includes ALL of the following 4 points:
            
            1. Distance to water (provide brief assessment with context)
            2. Distance to sea level (provide brief assessment with context)
            3. Distance to sea level: [X] m (only the numerical distance)
            4. Distance to water: [X] m (only the numerical distance)

            Keep the response concise and informative. Return the distance in metres as a number only with no additional assessment.
            """

            response = self.client.chat.completions.create(
                # model="gpt-4.1-2025-04-14",
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides location risk assessments."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=500
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error analyzing location: {str(e)}"
