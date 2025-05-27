from agents import Agent, Runner, set_tracing_disabled
from assistant_agent import dlims_supervisor
from typing import cast
import asyncio
import chainlit as cl


#load environment variables from .env file

set_tracing_disabled(disabled=True)

# Chainlit UI Startup Greeting(While opening Chainlit UI)
@cl.on_chat_start # This function is called when the chat starts
async def start():
    # Add Persistance in the Chainlit UI by using Chat History Through User_Session
    cl.user_session.set("chat_history", [])
    # add Agent Assistant in the User Session 
    cl.user_session.set("dlims_supervisor", dlims_supervisor)
    await cl.Message(
        content="Hello! I am your DLIMS AI assistant. How can I help you?"
    ).send()
# Conversation Chat start message content
@cl.on_message
async def main(message: cl.Message):
    # Get the chat history from the user session
    history = cl.user_session.get("chat_history") or []
    print(f"Chat History: {history}")
    # Get the assistant from the user session
    dlims_supervisor : Agent = cast(Agent, cl.user_session.get("dlims_supervisor"))

   
    # Get the user input from the message
    user_input = message.content
    print(f"User Input: {user_input}")
     # Add the user message to the chat history
    history.append({"role": "user", "content": user_input})
    print(f"Chat History After User Input: {history}")
    # Create a new Message Object for Streaming 
    msg = cl.Message(content="DLIMS : ")
    await msg.send()
################################# WITHOUT STREAM ############################################
    # Run the Runner Agent with the user input
    # response = await Runner.run(starting_agent= assistant, input= history)
    # llm_response = response.final_output
#############################################################################################
################################# WITH STREAM ############################################

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        result = Runner.run_streamed(starting_agent = dlims_supervisor,
                    input=history)
         # Stream the response token by token
        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
                token = event.data.delta
                await msg.stream_token(token)  
        ######################################################### 
        # Append the assistant's response to the history.
        history.append({"role": "assistant", "content": msg.content})

        # Update the message content with the final response
        
        await msg.update()
        # Update the session with the new history. overwrite the old history
        cl.user_session.set("chat_history", history)

        # Optional: Log the interaction
        print(f"User: {message.content}")
        print(f"Assistant: {msg.content}")

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")
        ################################################
    # Run the Runner Agent with the user input
    # response = Runner.run_streamed(starting_agent= assistant, input= history)
    # # Stream the response token by token
    # async for events in response.stream_events():
    #     if events.type == "raw_response_events" and hasattr(events.data,"delta" ):
    #         token = events.data.delta
    #         await message.stream_token(token)    

    # #############################################################################################
    # # Add the assistant message to the chat history
    # history.append({"role": "assistant", "content": msg.content})
    # print(f"Chat History After Assistant Response: {history}")
    # await msg.update() # Update the message in the UI
    # # Update the chat history in the user session
    # cl.user_session.set("chat_history", history)
    # await cl.Message(
    #     content=f"Assistant: {llm_response}"
    # ).send()
# Define Main Function to Run the Runner with Agent Assistant
# async def main():
#     response = await Runner.run(starting_agent= assistant, input= "What is the capital of Pakistan?")
#     print(response.final_output)

# if __name__ == "__main__":
#     asyncio.run(main())

