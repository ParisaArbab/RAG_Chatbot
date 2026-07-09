RAG CHATBOT PROJECT EXPLANATION
================================

Project name:
rag-chatbot

Short description:
This project is a simple RAG chatbot API. RAG means Retrieval-Augmented Generation.
The user uploads documents, the app stores the document content in a vector database,
and then the user can ask questions about those documents.

Main technologies:
- FastAPI: creates the API endpoints.
- LangChain: manages document loading, splitting, retrieval, and LLM response flow.
- ChromaDB: local vector database for development.
- Pinecone: cloud vector database option for production.
- OpenAI: creates embeddings and generates answers.


PROJECT FOLDER STRUCTURE
========================

rag-chatbot/

1. app/
   This is the main application folder. Most Python code is inside this folder.

2. app/__init__.py
   This file makes the app folder a Python package.
   It can be empty, but it helps Python import files from this folder.

3. app/main.py
   This is the main FastAPI file.
   It creates the API application and defines the endpoints.

   Important endpoints:
   - GET /health
     Checks if the API is running.

   - POST /ingest
     Uploads PDF, TXT, or Markdown files.
     It saves the files, loads their content, splits the text into chunks,
     and stores those chunks in the vector database.

   - POST /chat
     Accepts a user question.
     It retrieves relevant document chunks and generates an answer.

4. app/config.py
   This file reads settings from the .env file.
   Examples of settings:
   - OPENAI_API_KEY
   - VECTOR_DB
   - CHROMA_PERSIST_DIR
   - PINECONE_API_KEY
   - CHAT_MODEL
   - EMBEDDING_MODEL
   - CHUNK_SIZE
   - TOP_K

   This makes the project easy to configure without changing the code.

5. app/document_loader.py
   This file loads uploaded documents.
   It supports:
   - PDF files
   - TXT files
   - Markdown files

   It also splits large documents into smaller text chunks.
   Smaller chunks help the retrieval system find the most relevant text.

6. app/vector_store.py
   This file creates the vector database connection.

   If VECTOR_DB=chroma:
   - The app uses ChromaDB locally.
   - Data is stored in the chroma_db folder.

   If VECTOR_DB=pinecone:
   - The app uses Pinecone in the cloud.
   - The Pinecone API key and index name must be added to .env.

   This file also creates OpenAI embeddings.
   Embeddings convert text into numerical vectors for similarity search.

7. app/rag_chain.py
   This file contains the main RAG logic.

   Steps:
   - Receive the user's question.
   - Search the vector database for similar document chunks.
   - Build a context from those chunks.
   - Send the context and question to the LLM.
   - Return the answer and source previews.

   The prompt tells the model to answer only from uploaded documents.
   If the answer is not found, it says it does not know based on the uploaded documents.

8. app/schemas.py
   This file defines request and response formats using Pydantic.

   It includes:
   - ChatRequest: input question for /chat
   - ChatResponse: chatbot answer and sources
   - Source: document source information
   - IngestResponse: upload result for /ingest

9. data/uploads/
   Uploaded files are saved here.
   The app creates this folder automatically if it does not exist.

10. chroma_db/
   Local ChromaDB data is saved here.
   This folder is used only when VECTOR_DB=chroma.

11. requirements.txt
   This file lists all Python packages needed to run the project.
   You install them with:
   pip install -r requirements.txt

12. .env.example
   This is an example environment file.
   You should copy it to .env and add your real API keys.

13. .gitignore
   This file tells Git which files should not be uploaded to GitHub.
   For example, .env should not be uploaded because it contains secret keys.

14. Dockerfile
   This file is used to run the project inside Docker.
   Docker helps run the app in a clean and consistent environment.

15. sample_notes.txt
   This is a small sample text file.
   You can use it to test document upload and chatbot questions.

16. README.md
   This is the main project documentation in Markdown format.
   It explains setup, endpoints, and usage examples.

17. README_SIMPLE.txt
   This file explains the project in very simple English.
   It explains each file and how to run the project.


HOW THE CHATBOT WORKS
=====================

1. The user uploads a document using /ingest.
2. The document is saved in data/uploads.
3. LangChain loads the document.
4. The document is split into small chunks.
5. OpenAI creates embeddings for each chunk.
6. The chunks and embeddings are stored in ChromaDB or Pinecone.
7. The user asks a question using /chat.
8. The app searches for the most relevant chunks.
9. The LLM receives the question plus the retrieved chunks.
10. The LLM generates an answer based on the uploaded documents.


HOW TO RUN LOCALLY WITH CHROMADB
================================

Step 1: Open terminal inside the project folder.

cd rag-chatbot

Step 2: Create a virtual environment.

For macOS or Linux:
python -m venv .venv
source .venv/bin/activate

For Windows:
python -m venv .venv
.venv\Scripts\activate

Step 3: Install dependencies.

pip install -r requirements.txt

Step 4: Create the .env file.

For macOS or Linux:
cp .env.example .env

For Windows:
copy .env.example .env

Step 5: Open the .env file and add your OpenAI API key.

Example:
OPENAI_API_KEY=your_openai_api_key_here
VECTOR_DB=chroma
CHROMA_PERSIST_DIR=./chroma_db
COLLECTION_NAME=rag_documents

Step 6: Run the FastAPI app.

uvicorn app.main:app --reload

Step 7: Open the API docs in your browser.

http://127.0.0.1:8000/docs

Step 8: Test the API.

First, use /ingest to upload a PDF, TXT, or Markdown file.
Then, use /chat to ask a question about the uploaded file.


HOW TO UPLOAD A FILE USING CURL
===============================

Example:

curl -X POST "http://127.0.0.1:8000/ingest" \
  -F "files=@sample_notes.txt"

You can upload more than one file:

curl -X POST "http://127.0.0.1:8000/ingest" \
  -F "files=@sample_notes.txt" \
  -F "files=@another_file.pdf"


HOW TO ASK A QUESTION USING CURL
================================

Example:

curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is this document about?"}'

The response includes:
- answer
- sources
- content previews from retrieved chunks


HOW TO RUN WITH PINECONE
========================

Step 1: Create a Pinecone account and get your Pinecone API key.

Step 2: Edit the .env file.

Use this configuration:

OPENAI_API_KEY=your_openai_api_key_here
VECTOR_DB=pinecone
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=rag-chatbot-index
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1

Step 3: Run the app.

uvicorn app.main:app --reload

The app will use Pinecone instead of ChromaDB.
If the Pinecone index does not exist, the app tries to create it.


HOW TO RUN WITH DOCKER
======================

Step 1: Make sure Docker is installed.

Step 2: Create your .env file and add your API keys.

Step 3: Build the Docker image.

docker build -t rag-chatbot .

Step 4: Run the Docker container.

docker run --env-file .env -p 8000:8000 rag-chatbot

Step 5: Open the API docs.

http://127.0.0.1:8000/docs


IMPORTANT ENVIRONMENT VARIABLES
===============================

OPENAI_API_KEY
Your OpenAI API key. This is required.

VECTOR_DB
Choose the vector database.
Use chroma for local development.
Use pinecone for cloud vector storage.

CHROMA_PERSIST_DIR
Folder where local ChromaDB data is saved.

COLLECTION_NAME
Name of the ChromaDB collection.

PINECONE_API_KEY
Your Pinecone API key. Required only when VECTOR_DB=pinecone.

PINECONE_INDEX_NAME
Name of the Pinecone index.

CHAT_MODEL
OpenAI chat model used for answer generation.

EMBEDDING_MODEL
OpenAI embedding model used to convert text into vectors.

CHUNK_SIZE
Maximum size of each text chunk.

CHUNK_OVERLAP
Number of overlapping characters between chunks.

TOP_K
Number of document chunks retrieved for each question.


EXPLANATION
============================

I built a RAG chatbot API using FastAPI, LangChain, and a vector database.
The user can upload documents. The system splits the documents into chunks,
creates embeddings, and stores them in ChromaDB or Pinecone. When the user asks
a question, the system retrieves the most relevant chunks and sends them to the
LLM as context. This helps the model answer based on the uploaded documents and
reduces hallucination.


COMMON PROBLEMS AND FIXES
=========================

Problem: OPENAI_API_KEY error
Fix: Make sure you created a .env file and added your real OpenAI API key.

Problem: Upload file error
Fix: Make sure the file type is PDF, TXT, or MD.

Problem: Module not found error
Fix: Run pip install -r requirements.txt inside the activated virtual environment.

Problem: Pinecone API key error
Fix: Use VECTOR_DB=chroma if you do not want to use Pinecone.
If you want Pinecone, add PINECONE_API_KEY in .env.

Problem: API does not open
Fix: Make sure uvicorn is running and open http://127.0.0.1:8000/docs.
