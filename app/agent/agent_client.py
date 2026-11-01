from openai import AsyncOpenAI
from app.core.config import get_settings

settings = get_settings()

class AgnetClient():
    
    def __init__(self):
        self.settings = settings
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        
    async def sent_request_agent(self, message_data: dict):
        
        message = (message_data.message if message_data else None)
        if message is not None:
            response = self.client.responses.create(
                model=self.settings.model_openai_gpt,
                input=message,
            )
            return {
                "response": response.output_text,
                "status_code": 200
                }