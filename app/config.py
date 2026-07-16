from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from .env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    openai_api_key: str

    vector_db: str = "chroma"  # chroma or pinecone

    chroma_persist_dir: str = "./chroma_db"
    collection_name: str = "rag_documents"

    pinecone_api_key: str | None = None
    pinecone_index_name: str = "rag-chatbot-index"
    pinecone_cloud: str = "aws"
    pinecone_region: str = "us-east-1"

    chat_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    temperature: float = 0

    chunk_size: int = 1000
    chunk_overlap: int = 150
    top_k: int = 4


@lru_cache
def get_settings() -> Settings:
    return Settings()
