import httpx

from app.core.config import get_settings

settings = get_settings()

class EmailServise:
    
    async def send_otp_email(self, email: str, code: str, otp_ttl: int):
        
        headers = {
            "Authorization": f"Bearer {settings.resend_api_key}",
            "Content_Type": "application/json"
        }
        pyload = {
            
            "from": f"{settings.mail_default_sender}",
            "to": [email],
            "subject": f"{settings.email_subject}",
            "html": f"""
            <html>
                <body>
                    <h2>Password Reset</h2>
                    <p>{settings.email_template}</p>
                    <h1>{code}</h1>
                    <p>This code expires in {ttl_code} minutes</p>
                </body>
            </html>
            """
        
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url="https://api.resend.com/emails",
                headers=headers,
                json=pyload
            )
        
        return response
        