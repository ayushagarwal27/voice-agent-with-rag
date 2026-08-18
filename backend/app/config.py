from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # MongoDB Settings
    MONGO_URL: str
    DB_NAME: str = "live_db"

    # LLM Model
    OPENAI_API_KEY:str
    OPENAI_MODEL:str

    # RAG
    EMBEDDING_MODEL:str
    CHUNK_SIZE:int
    CHUNK_OVERLAP:int
    VECTOR_INDEX_NAME:str = "vector_index"
    DOCUMENT_CHUNKS_COLLECTION:str= "document_chunks"

    # Voice
    DEEPGRAM_API_KEY:str
    CARTESIA_API_KEY:str
    CARTESIA_VOICE_ID:str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()