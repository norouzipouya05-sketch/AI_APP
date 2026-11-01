from fastapi import Depends

from app.agent.agent_client import AgnetClient

async def agent_client() -> AgnetClient:
    return AgnetClient()