from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # MongoDB Settings
    MONGO_URL: str
    DB_NAME: str = "live_db"

    OPENAI_API_KEY:str
    EMBEDDING_MODEL:str

    CHUNK_SIZE:int
    CHUNK_OVERLAP:int
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()