from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.document_loader import SUPPORTED_EXTENSIONS, load_document, split_documents
from app.rag_chain import ask_question
from app.schemas import ChatRequest, ChatResponse, IngestResponse
from app.vector_store import get_vector_store

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="RAG Chatbot API",
    description="A simple RAG chatbot using LangChain, FastAPI, and ChromaDB or Pinecone.",
    version="1.0.0",
)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/ingest", response_model=IngestResponse)
async def ingest_files(files: list[UploadFile] = File(...)):
    """Upload PDF, TXT, or Markdown files and add them to the vector database."""
    all_chunks = []
    saved_files = []

    for file in files:
        extension = Path(file.filename).suffix.lower()
        if extension not in SUPPORTED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {extension}. Use PDF, TXT, or MD.",
            )

        safe_name = f"{uuid4().hex}_{Path(file.filename).name}"
        file_path = UPLOAD_DIR / safe_name

        content = await file.read()
        file_path.write_bytes(content)
        saved_files.append(file.filename)

        documents = load_document(str(file_path))
        chunks = split_documents(documents)
        all_chunks.extend(chunks)

    if not all_chunks:
        raise HTTPException(status_code=400, detail="No valid document chunks found.")

    vector_store = get_vector_store()
    vector_store.add_documents(all_chunks)

    return IngestResponse(
        message="Documents ingested successfully.",
        files=saved_files,
        chunks_added=len(all_chunks),
    )


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Ask a question about the uploaded documents."""
    try:
        result = ask_question(request.question)
        return ChatResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
