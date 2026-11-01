from pydantic import BaseModel, Field
from typing import Optional

class ResponseAgent(BaseModel):
    response: str 
    status_code: int
    
class AuthResponse(BaseModel):
    refresh_token: str = Field(default=None, min_length=2)
    access_token: str = Field(default=None, min_length=2)
    token_type: str = Field(default=None, min_length=2)
    
class OTPResponse(BaseModel):
    message: Optional[str] = Field(default=None)
    identifier: Optional[str] = Field(default=None)
    ttl: Optional[int] = Field(default=None)
    code: Optional[str] = Field(default=None)
    
class OTPResponseVerify(BaseModel):
    challenge_token: Optional[str] = Field(default=None)
    ttl: Optional[str] = Field(default=None)
    