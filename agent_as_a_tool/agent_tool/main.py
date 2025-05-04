import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, AsyncOpenAI
# from openai import AsyncOpenAI
from agents.run import RunConfig
from agents.tool import function_tool

load_dotenv(find_dotenv())  # Load environment variables from .env file

set_tracing_disabled(disabled=True) # Disable tracing for the agent

# #setup Configuration for model with Gemini API key

gemini_api_key = os.getenv("GEMINI_API_KEY")
if gemini_api_key is None:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")
print("Using Gemini API key")  
# Provider
external_client= AsyncOpenAI(api_key=gemini_api_key,
                             base_url="https://generativelanguage.googleapis.com/v1beta/openai/",)
print("Using external client")

#Setup Model 
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)
#######################################################################################
# Define a shoping Agent
# shoping_agent = Agent (
#     name = "Shopping Assistant",    
#     instructions = "You are a shopping assistant. Help the user find the best products for their needs.", 
# )

# support_agent = Agent (
#     name = "Support Assistant",
#     instructions = "You are a support assistant. Help the user with their questions.",
# )

# # Convert Agent into a tool
# shoping_tool = shoping_agent.as_tool(
#     tool_name="Shopping Assistant",
#     tool_description="You are a shopping assistant. Help the user find the best products for their needs.",
# )
# support_tool = support_agent.as_tool(
#     tool_name="Support Assistant",
#     tool_description="You are a support assistant. Help the user with their questions.",
# )
#################################################################################################################
# Create  Tools
################################################################################################################
# Create a function tool for getting weather information
@function_tool("get_weather")
def get_weather(location: str, unit: str = "C") -> str:
  """
  Fetch the weather for a given location, returning a short description.
  """
  # Example logic
  return f"The weather in {location} is 22 degrees {unit}."
# create a tool to find student based on roll number
@function_tool("piaic_student_finder")
def student_finder(student_roll: int) -> str:
  """
  find the PIAIC student based on the roll number
  """
  data = {1: "Qasim",
          2: "Sir Zia",
          3: "Daniyal"}

  return data.get(student_roll, "Not Found")
# Create a triage Agent that uses the tools
triage_agent = Agent(
    name = "Triage Assistant",
    instructions = "You are a triage assistant. Help the user find the best tool for their needs.",
    tools=[get_weather, student_finder],
    model=model,
)

# run a triage agent with a user input
async def main():
    result = await Runner.run(starting_agent=triage_agent, input="what is the weather in Karachi? and find me a student with roll number 2",  
                            run_config=config)
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
