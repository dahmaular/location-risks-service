import os
from dotenv import load_dotenv


class Config:

    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        if not self.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Please create a .env file with your OpenAI API key."
            )

    def get_openai_api_key(self):
        """Return the OpenAI API key."""
        return self.openai_api_key
