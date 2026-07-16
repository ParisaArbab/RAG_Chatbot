from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, examples=["What is this document about?"])


class Source(BaseModel):
    source: str
    page: int | None = None
    content_preview: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]


class IngestResponse(BaseModel):
    message: str
    files: list[str]
    chunks_added: int
