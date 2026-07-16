# Demo Script

Use this short demo for GitHub, LinkedIn, or interviews.

## 30-second demo flow

1. Start the API.

```bash
uvicorn app.main:app --reload
```

2. Open Swagger docs.

```text
http://127.0.0.1:8000/docs
```

3. Upload `sample_notes.txt` to `/ingest`.

4. Ask this question in `/chat`.

```json
{
  "question": "What is RAG?"
}
```

5. Show the response with answer and sources.

## What to say in an interview

This project demonstrates a document question-answering system. The user uploads documents, the system converts them into embeddings, stores them in a vector database, retrieves the most relevant chunks, and uses an LLM to generate a grounded answer.
