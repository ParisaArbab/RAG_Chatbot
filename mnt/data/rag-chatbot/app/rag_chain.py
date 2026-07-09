from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.config import get_settings
from app.vector_store import get_vector_store

SYSTEM_PROMPT = """
You are a helpful RAG chatbot.
Answer the user question using only the context below.
If the answer is not in the context, say: "I do not know based on the uploaded documents."
Keep the answer clear and simple.

Context:
{context}
"""


def format_docs(docs) -> str:
    return "\n\n".join(
        f"Source: {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
        for doc in docs
    )


def ask_question(question: str) -> dict:
    settings = get_settings()
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": settings.top_k})

    docs = retriever.invoke(question)
    context = format_docs(docs)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "Question: {question}"),
        ]
    )

    llm = ChatOpenAI(
        model=settings.chat_model,
        temperature=settings.temperature,
        api_key=settings.openai_api_key,
    )

    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"context": context, "question": question})

    sources = []
    for doc in docs:
        sources.append(
            {
                "source": doc.metadata.get("source", "unknown"),
                "page": doc.metadata.get("page"),
                "content_preview": doc.page_content[:250].replace("\n", " "),
            }
        )

    return {"answer": answer, "sources": sources}
