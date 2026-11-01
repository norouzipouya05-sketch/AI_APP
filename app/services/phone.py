import httpx

from app.core.config import get_settings

settings = get_settings()

class PhoneService:
    
    async def send_otp_phone(self, phone: str, code: str):
        
        otp_request_pyload = {
            "receptor": str(phone),
            "message": str(code)
        }
        
        async with httpx.AsyncClient(base_url="https://api.kavenegar.com") as client:
            response = await client.post(
                url=f"/v1/{settings.number_otp_api_key}/sms/send.json",
                json=otp_request_pyload
            )
            
        return response