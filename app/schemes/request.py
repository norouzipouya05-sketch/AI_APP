from pydantic import BaseModel, Field
from typing import Optional

class OTPRequest(BaseModel):
    phone: Optional[str] = Field(min_length=4, max_length=15)
    email: Optional[str] = Field(min_length=1)
    
class OTPVeifyRequest(BaseModel):
    phone: str = Field(min_length=4, max_length=15)
    code: str = Field(min_length=4, max_length=4)

class SendMessage(BaseModel):
    message: str = Field(min_length=1)
    
class LoginRequest(BaseModel):
    phone: str = Field(min_length=10, max_length=15)
    email: str = Field(min_length=1)
    password: str = Field(min_length=5, max_length=12)
        
    
class RegisterUser(BaseModel):
    phone: str = Field(min_length=10, max_length=15)
    email: str = Field(min_length=1)
    password: str = Field(min_length=5, max_length=12)
    challenge_token: str = Field(min_length=6, max_length=6)
    
class LogoutUser(BaseModel):
    token: str = Field(min_length=1)
    
class RefreshToken(BaseModel):
    refresh_token: str = Field(min_length=1)