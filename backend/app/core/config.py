from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str 
    OPENAI_API_KEY: str  
    SECRET_KEY: str 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @property
    def database_url(self) -> str:
        return self.DATABASE_URL

    class Config:
        env_file = ".env"


settings = Settings()


