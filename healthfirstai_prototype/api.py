from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from healthfirstai_prototype.nutrition_agent import init_agent

app = FastAPI()


class UserInput(BaseModel):
    user_input: str
    uid: int
    session_id: str
    verbose: bool = False


@app.get("/")
async def root():
    return {"status": "Web server is running"}


@app.post("/chat_agent/")
async def chat_agent(user_input: UserInput):
    """
    Initiate an interactive chat session.

    POST Parameters:
    - user_input (str): The user's input text for the conversation. It's a required field.
    - uid (int): The ID of the user. It's a required field.
    - session_id (str): The session ID for maintaining conversation history. It's a required field.
    - verbose (bool, optional): If set to True, the function provides more detailed output. Default is False.

    Raises HTTPException:
    - status_code: 404
    - detail: "User input not provided" / "User ID not provided" / "Session ID not provided"
    """
    if not user_input.user_input:
        raise HTTPException(status_code=404, detail="User input not provided")
    if not user_input.uid:
        raise HTTPException(status_code=404, detail="User ID not provided")
    if not user_input.session_id:
        raise HTTPException(status_code=404, detail="Session ID not provided")

    agent_object = init_agent(
        user_input.user_input,
        user_input.uid,
        user_input.session_id,
        verbose=user_input.verbose,
    )
    return {"agent_response": agent_object(user_input.user_input)}


# TODO: Add endpoint to get similar foods

# TODO: Add endpoint to get meal info

# TODO: Add endpoint to get food info

# TODO: Add endpoint to confirm diet plan changes
