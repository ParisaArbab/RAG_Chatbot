from pathlib import Path
from typing import Iterable

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import get_settings

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


def load_document(file_path: str) -> list[Document]:
    """Load one PDF, TXT, or Markdown file into LangChain documents."""
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {extension}. Use PDF, TXT, or MD.")

    if extension == ".pdf":
        loader = PyPDFLoader(str(path))
        docs = loader.load()
    else:
        loader = TextLoader(str(path), encoding="utf-8")
        docs = loader.load()

    for doc in docs:
        doc.metadata["source"] = path.name

    return docs


def split_documents(documents: Iterable[Document]) -> list[Document]:
    settings = get_settings()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(list(documents))
