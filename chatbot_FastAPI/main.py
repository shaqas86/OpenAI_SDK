import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from assistant_agent import panacloud_agent
from agents import Runner
from schema import Message, Response, Metadata
from openai.types.responses import ResponseTextDeltaEvent

app= FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

# Endpoint to get assistant's response
@app.post("/assistant/{query}")
async def get_assistant_response(query: str):
    print(f"Received query: {query}")
    response =await Runner.run(starting_agent=panacloud_agent, input=query)
    return {"response": response.final_output}

@app.post("/chat/", response_model=Response)
async def chat(message: Message):
    if not message.text.strip():
        raise HTTPException(
            status_code=400, detail="Message text cannot be empty")

    # Use the OpenAI Agents SDK to process the message
    result = await Runner.run(panacloud_agent, input=message.text)
    reply_text = result.final_output  # Get the agent's response

    return Response(
        user_id=message.user_id,
        reply=reply_text,
        metadata=Metadata()
    )
#streming
async def stream_response(message: Message):
    result = Runner.run_streamed(panacloud_agent, input=message.text)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
            # Serialize dictionary to JSON string
            chunk = json.dumps({"chunk": event.data.delta})
            yield f"data: {chunk}\n\n"
            
@app.post("/chat/stream", response_model=Response)
async def chat_stream(message: Message):
    if not message.text.strip():
        raise HTTPException(
            status_code=400, detail="Message text cannot be empty")

    return StreamingResponse(
        stream_response(message),
        media_type="text/event-stream"
    )