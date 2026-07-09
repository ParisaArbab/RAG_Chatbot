# RAG Chatbot, LangChain + FastAPI + ChromaDB/Pinecone

This is a simple Retrieval-Augmented Generation chatbot API.

It can:

1. Upload PDF, TXT, or Markdown files.
2. Split files into small chunks.
3. Store chunks in ChromaDB or Pinecone.
4. Retrieve relevant chunks for a user question.
5. Generate an answer using an LLM.
6. Return the answer with source previews.

## Tech stack

- FastAPI, API backend
- LangChain, RAG orchestration
- ChromaDB, local vector database
- Pinecone, cloud vector database option
- OpenAI, chat model and embedding model

FastAPI supports file upload using `UploadFile`, and uploaded files require `python-multipart`. LangChain provides vector store integrations with a common interface such as adding documents and similarity search. Chroma is good for local development, while Pinecone is better for managed production-scale vector search.

## Project structure

```text
rag-chatbot/
├── app/
│   ├── main.py              # FastAPI routes
│   ├── config.py            # Environment settings
│   ├── document_loader.py   # Load and split files
│   ├── vector_store.py      # ChromaDB/Pinecone factory
│   ├── rag_chain.py         # Retrieval and answer generation
│   └── schemas.py           # Request/response models
├── data/uploads/            # Uploaded files
├── chroma_db/               # Local Chroma database
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md
```

## 1. Setup

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows
```

Install packages:

```bash
pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

Add your OpenAI key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 2. Run with ChromaDB locally

In `.env`, keep:

```env
VECTOR_DB=chroma
CHROMA_PERSIST_DIR=./chroma_db
COLLECTION_NAME=rag_documents
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## 3. Upload documents

Using curl:

```bash
curl -X POST "http://127.0.0.1:8000/ingest" \
  -F "files=@sample.pdf" \
  -F "files=@notes.txt"
```

Example response:

```json
{
  "message": "Documents ingested successfully.",
  "files": ["sample.pdf", "notes.txt"],
  "chunks_added": 18
}
```

## 4. Ask a question

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the main idea of the uploaded document?"}'
```

Example response:

```json
{
  "answer": "The document explains ...",
  "sources": [
    {
      "source": "sample.pdf",
      "page": 0,
      "content_preview": "The document explains ..."
    }
  ]
}
```

## 5. Use Pinecone instead of ChromaDB

In `.env`, change:

```env
VECTOR_DB=pinecone
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=rag-chatbot-index
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
```

Then run the same FastAPI app:

```bash
uvicorn app.main:app --reload
```

The app will create the Pinecone index if it does not exist.

## 6. Docker

Build the image:

```bash
docker build -t rag-chatbot .
```

Run it:

```bash
docker run --env-file .env -p 8000:8000 rag-chatbot
```

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check if API is running |
| POST | `/ingest` | Upload and index documents |
| POST | `/chat` | Ask a question using RAG |

## How RAG works here

1. User uploads documents.
2. The app loads the documents.
3. Documents are split into chunks.
4. Each chunk is converted to an embedding.
5. Embeddings are saved in ChromaDB or Pinecone.
6. When the user asks a question, similar chunks are retrieved.
7. The LLM answers using only those retrieved chunks.

## Notes for interview explanation

You can explain it like this:

> I built a RAG chatbot API using FastAPI and LangChain. The user can upload documents, and the system splits them into chunks, creates embeddings, and stores them in a vector database. When the user asks a question, the app retrieves the most relevant chunks and sends them to the LLM as context. This reduces hallucination because the answer is grounded in the uploaded documents. I made the vector database configurable, so the project can run locally with ChromaDB or in the cloud with Pinecone.

## Possible improvements

- Add user authentication.
- Add document deletion.
- Add chat history.
- Add streaming responses.
- Add reranking for better retrieval.
- Add frontend using React.
- Add tests with pytest.
