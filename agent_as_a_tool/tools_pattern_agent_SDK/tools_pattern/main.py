import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from agents import Agent, RunConfig, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from agents.tool import function_tool
from tavily import TavilyClient

load_dotenv(find_dotenv())

set_tracing_disabled(disabled=True)

# setup gemini api key
gemini_api_key = os.getenv("GEMINI_API_KEY")
if gemini_api_key is None:
    raise ValueError("GEMINI_API_KEY environment variable not set.")
print("Gemini API Key:>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

# setup tavily api key
tavily_api_key = os.getenv("TAVILY_API_KEY")
if tavily_api_key is None:
    raise ValueError("TAVILY_API_KEY environment variable not set.")
# load Base URL from environment variable or use default
base_url = os.getenv("BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
# Setup Provider 
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=base_url,
)

# Setup Model

model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.0-flash",
 )

# Setup Run Config
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Setup Tavily Client
tavily_client = TavilyClient(api_key= tavily_api_key)
# Setup Tavily Function Tool
@function_tool()
def search_online(query: str):
    """Search the web for the given query."""
    return tavily_client.search(query=query)
#########################################################################################
# Agent Configuration using Tavily Function Tool
#########################################################################################
# Setup Agent
agent = Agent(
    name="SearchAssistant",
    instructions="You can search online or simply answer. Response with an Emoji",
    tools=[search_online], # add tools here
    model=model
)

# result = Runner.run_sync(agent, "call search tool and tell what is the todays dollar to pkr price rate")
# print(result.final_output)
###############################################################################################
# Ecommerce Shoping Agent
###############################################################################################
import requests
response = requests.get('https://fakestoreapi.com/products')
# print(response.json())

@function_tool
def get_all_products_in_store():
  response = requests.get('https://fakestoreapi.com/products')
  return response.json()

# Add to Cart Agent

add_to_cart_agent = Agent(
    name="Cart Agent",
    instructions="You can manage user cart",
    model=model
)

# Add Shoping Agent 
shopping_agent = Agent(
    name="Shopping Agent",
    instructions="You can search online or simply answer. Response with an Emoji",
    tools=[
         # add tools here
        get_all_products_in_store,
        add_to_cart_agent.as_tool(
            tool_name="cart_managing_tool",
            tool_description="You manage user cart"
            ),
        agent.as_tool(
            tool_name="search_tool",
            tool_description="You search online or simply answer. Response with an Emoji"
            )

        ], # add tools here
    model=model
)

# set in main function in async await to run the agent until user press exit or Ctrl+C
async def main():
    # run agent in loop until user press exit or Ctrl+C
    while True:
        # get user input
        try: 
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting...")
                break
            # run agent
            result = await Runner.run(starting_agent=shopping_agent, input=user_input)
            print(result.final_output)  
        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            print(e)


if __name__ == "__main__":
    print("Starting agent...")
    print("Press Ctrl+C to exit.")
    asyncio.run(main())

         

    