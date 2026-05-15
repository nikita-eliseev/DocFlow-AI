import os

from dotenv import load_dotenv
from openai import OpenAI
from app.core.config import settings

load_dotenv()

client = OpenAI(
    api_key=os.getenv(settings.openai_api_key)
)