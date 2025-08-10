from dotenv import load_dotenv
import os

class Settings():
    def __init__(self) -> None:
        load_dotenv()
        self.llm_api_key = os.environ["GEMINI_API_KEY"]
        self.tavily_api_key = os.environ["TAVILY_API_KEY"]

options = Settings()