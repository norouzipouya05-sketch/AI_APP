from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )
    
    # AGENT
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    model_openai_gpt: str = Field("gpt-4o-mini", alias="MODEL_OPENAI_GPT")
    
    # JWT
    secret_key: str = Field("my_secret", alias="SECRET_KEY")
    access_token_expire: int = Field(60, alias="ACCESS_TOKEN_EXPIRE")
    refresh_token_expire: int = Field(30, alias="REFRESH_TOKEN_EXPIRE")
    jwt_algorithm: str = Field("HS256", alias="JWT_ALGORITHM")
    
    # DB
    db_driver: str = Field("postgresql+asyncpg", alias="DB_DRIVER")
    db_username: str = Field(..., alias="DB_USERNAME")
    db_password: str = Field(..., alias="DB_PASSWORD")
    db_server: str = Field("localhost", alias="DB_SERVER")
    db_port: str = Field(5432, alias="DB_PORT")
    db_name: str = Field(..., alias="DB_NAME")
    
    db_status_debug_logg: bool = Field(True, alias="DB_STATUS_DEBUG_LOGG")
    db_pool_size: int = Field(20, alias="DB_POOL_SIZE")
    db_max_overflow: int = Field(10, alias="DB_MAX_OVERFLOW")
    db_pool_recycle: int = Field(500, alias="DB_POOL_RECYCLE")
    
    # REDIS
    redis_url: str = Field("redis://localhost:6379/0", alias="REDIS_URL")
    redis_max_connection: int = Field(30, alias="REDIS_MAX_CONNECTION")
    otp_ttl_sec: int = Field(240, alias="OTP_TTL_SEC")
    
    # REDIS
    otp_request_cooldown_sec: int = Field(30, alias="OTP_REQUEST_COOLDOWN_SEC")
    number_otp_api_key: str = Field(None, alias="NUMBER_OTP_API_KEY")
    
    # Mail
    mail_default_sender: str = Field(
        "POUYA <no-reply@POUYA.ai>", alias="MAIL_DEFAULT_SENDER"
    )
    email_subject: str = Field(default="POUYA OTP Code", alias="EMAIL_SUBJECT")
    email_template: str = Field(default="Your OTP Code: ", alias="EMAIL_TEMPLATE")
    resend_api_key: str = Field(default="", alias="RESEND_API_KEY")
    
    # RATE LIMIT
    rate_limit_per_min: int = Field(60, alias="RATE_LIMIT_PER_MIN")
    rate_limit_authenticated: int = Field(alias="RATE_LIMIT_AUTHENTICATED")
    rate_limit_unauthenticated: int = Field(alias="RATE_LIMIT_UNAUTHENTICATED")


    
    @property
    def database_url(self) -> str:
        return f"{self.db_driver}://{self.db_username}:{self.db_password}@{self.db_server}:{self.db_port}/{self.db_name}"
    
@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
