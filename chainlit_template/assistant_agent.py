from agents import Agent, Runner, set_tracing_disabled
from llm_shared import litellm_model

#set up OpenAI Agent as Assistant 
assistant:Agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant.",
    model=litellm_model
)
