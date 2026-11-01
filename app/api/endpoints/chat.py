from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from app.agent.agent_client import AgnetClient
from app.schemes.request import SendMessage
from app.schemes.response import ResponseAgent

router = APIRouter(prefix="/agent", tags=["agent"])

@router.post("/send", response_model=ResponseAgent)
async def send_message(
    message_data: SendMessage,
    agent_client: Annotated[AgnetClient, Depends(AgnetClient)]
):
    try:
        result = await agent_client.sent_request_agent(message_data)
        return result
    except Exception as er:
        raise HTTPException(
            status_code=502,
            detail="errored"
        ) from er
    
    