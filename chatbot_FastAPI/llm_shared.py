import os
from dotenv import load_dotenv, find_dotenv
from agents.extensions.models.litellm_model import LitellmModel
import agentops
#load environment variables from .env file
load_dotenv(find_dotenv())
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
if AGENTOPS_API_KEY:
    print("AGENTOPS_API_KEY LOADED>>>>>>>>>>>>>>>>>>")
# Initialize AgentOps
agentops.init(AGENTOPS_API_KEY)
print("AgentOps initialized successfully.>>>>>>>>>>>>>>>>>>>>>>>>>>>")

#set up Gemini API key and model
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    print("GEMINI_API_KEY LOADED>>>>>>>>>>>>>>>>>>")
else:
    raise ValueError("GEMINI_API_KEY environment variable not set")

model = os.getenv("MODEL") or "gemini/gemini-2.0-flash"
if model is None:
    raise ValueError("MODEL environment variable not set")
print(f"Using model>>>>>>>>>>>>>>>>> {model}")

#set up Litellm Model
litellm_model = LitellmModel(model=model, api_key=GEMINI_API_KEY)