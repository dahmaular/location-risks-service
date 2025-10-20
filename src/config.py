import os
from dotenv import load_dotenv


class Config:

    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # API Security Configuration
        self.api_key = os.getenv("API_KEY", "4590afd6-c4ed-43f1-8f8d")
        self.vendor_id = os.getenv("VENDOR_ID", "c8w3e")

        if not self.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Please create a .env file with your OpenAI API key."
            )

    def get_openai_api_key(self):
        """Return the OpenAI API key."""
        return self.openai_api_key

    def get_api_key(self):
        """Return the API key for authentication."""
        return self.api_key

    def get_vendor_id(self):
        """Return the vendor ID for authentication."""
        return self.vendor_id

    def validate_credentials(self, provided_api_key, provided_vendor_id):
        """Validate provided credentials against configured values."""
        return (provided_api_key == self.api_key and
                provided_vendor_id == self.vendor_id)
