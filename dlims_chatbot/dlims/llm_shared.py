import os
from dotenv import load_dotenv, find_dotenv
from agents.extensions.models.litellm_model import LitellmModel
#load environment variables from .env file
load_dotenv(find_dotenv())
#set up Gemini API key and model
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY environment variable not set")

model = os.getenv("MODEL") or "gemini/gemini-2.0-flash"
if model is None:
    raise ValueError("MODEL environment variable not set")
print(f"Using model>>>>>>>>>>>>>>>>> {model}")

#set up Litellm Model
litellm_model = LitellmModel(model=model, api_key=GEMINI_API_KEY)