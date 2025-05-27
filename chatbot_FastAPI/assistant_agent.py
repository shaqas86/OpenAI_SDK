from agents import Agent, Runner, set_tracing_disabled,function_tool
from llm_shared import litellm_model
import asyncio
from agents.extensions.visualization import draw_graph
from datetime import datetime, UTC

#set up OpenAI Agent as Assistant 
# assistant:Agent = Agent(
#     name="assistant",
#     instructions="You are a helpful assistant.",
#     model=litellm_model
# )

# === Tool Functions ===

@function_tool
def get_current_time() -> str:
    """Returns the current time in UTC."""
    return datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
@function_tool
def draft_agreement() -> str:
    """Drafts an agreement."""
    return "Agreement drafted successfully."

@function_tool
def save_agreement() -> str:
    """Saves the agreement to the system."""
    return "Agreement saved successfully."

# === Leaf Agents ===
planner_agent = Agent(
    name="Planner",
    instructions="You are a helpful assistant for Planner queries.",
    model=litellm_model
)
planner_agent_tool=  planner_agent.as_tool(tool_name="use_planner", tool_description="Task planning with Planner agent")

devops_agent = Agent(
    name="DevOps",
    instructions="You are a helpful assistant for DevOps queries.",
    model=litellm_model
)
devops_agent_tool=  devops_agent.as_tool(tool_name="use_devops", tool_description="Infra/devops with DevOps agent")

web_agent = Agent(
    name="Web",
    instructions="You are a helpful assistant for Web-related queries.",
    model=litellm_model
)
# === AgenticAI ===
agentic_ai = Agent(
    name="AgenticAI",
    instructions="You are a coordinator AI. You use tools for planning and operations, and hand off UI tasks as needed.",
    tools=[
        planner_agent_tool,
        devops_agent_tool,get_current_time
    ],
    handoffs=[
        web_agent
    ],
    model=litellm_model
)

mobile_agent = Agent(
    name="Mobile",
    instructions="You are a helpful assistant for Mobile-related queries. You can handoff to the AgenticAI agent for deeper assistance.",
    model=litellm_model,
    handoffs=[agentic_ai]
)

# === PanaCloud Top-Level Agent ===
panacloud_agent = Agent(
    name="PanaCloud",
    instructions="You are the main assistant for Panacloud. You may use tools or delegate to other agents as needed.",
    tools=[draft_agreement, save_agreement,get_current_time],
    handoffs=[
        mobile_agent,
        web_agent,
        agentic_ai
    ],
    model=litellm_model
)

#async define main function
async def main():
    draw_graph(panacloud_agent,filename= "panacloud_agent.png")  # Visualize the agent hierarchy
    #create a runner
    response = await Runner.run(starting_agent=panacloud_agent, input="Hello, how can I help you today?")
    print(response.final_output)  # Print the final output from the agent
if __name__ == "__main__":
    asyncio.run(main())

    
    