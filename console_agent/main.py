import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, set_tracing_disabled
from openai import AsyncOpenAI
from agents.extensions.models.litellm_model import LitellmModel
import asyncio

#load envoirnemt variable from .env file

load_dotenv(find_dotenv())
set_tracing_disabled(disabled=True)

#Set Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Set Model from .env file
model = os.getenv("MODEL") or "gemini/gemini-2.0-flash"

print(f"Using model >>>> : {model}")
#Set Litellm model instance for using Gemini API, and Model name
litellm_model = LitellmModel(
    model=model,
    api_key=GEMINI_API_KEY
)

# Agent for Assistance 
agent : Agent = Agent(
    name="Gemini Assistant",
    instructions="A helpful assistant that can answer questions and provide information.",
    model=litellm_model,
)
# set in main function in async await to run the agent until user press exit or Ctrl+C
async def main():
    #run agent in loop until user press exit or Ctrl+C
    while True:
        try:
            #get user input
            user_input = input("You: ")
            #run agent
            response= await Runner.run(starting_agent=agent, input=user_input)
            print(response.final_output)

        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            break
    

if __name__ == "__main__":
    #run main function in async await
    print("Starting Gemini Assistant...")
    print("Press Ctrl+C to exit.")
    asyncio.run(main())