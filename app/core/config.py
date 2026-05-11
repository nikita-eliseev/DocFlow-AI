from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = "dev"
    debug: bool = False
    
    database_url: str
    
    openai_api_key: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )
    
settings = Settings()