from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from app.config import get_settings


def get_embeddings() -> OpenAIEmbeddings:
    settings = get_settings()
    return OpenAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.openai_api_key,
    )


def get_vector_store() -> VectorStore:
    """Create a vector store based on VECTOR_DB in .env."""
    settings = get_settings()
    embeddings = get_embeddings()

    if settings.vector_db.lower() == "chroma":
        return Chroma(
            collection_name=settings.collection_name,
            embedding_function=embeddings,
            persist_directory=settings.chroma_persist_dir,
        )

    if settings.vector_db.lower() == "pinecone":
        if not settings.pinecone_api_key:
            raise ValueError("PINECONE_API_KEY is required when VECTOR_DB=pinecone")

        pc = Pinecone(api_key=settings.pinecone_api_key)
        existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

        if settings.pinecone_index_name not in existing_indexes:
            pc.create_index(
                name=settings.pinecone_index_name,
                dimension=1536,  # text-embedding-3-small dimension
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=settings.pinecone_cloud,
                    region=settings.pinecone_region,
                ),
            )

        index = pc.Index(settings.pinecone_index_name)
        return PineconeVectorStore(index=index, embedding=embeddings)

    raise ValueError("VECTOR_DB must be either 'chroma' or 'pinecone'")
