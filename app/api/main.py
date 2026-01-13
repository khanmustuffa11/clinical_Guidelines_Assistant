from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware


from app.rag.generator import ask_guidelines

app = FastAPI(
    title="Clinical Guidelines RAG",
    version="1.1"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    question: str
    answer: str
    sources: List[str]
    
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
def ask(query: Query):
    result = ask_guidelines(query.question)
    return {
        "question": query.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }
