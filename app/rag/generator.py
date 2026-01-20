from typing import Optional
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from app.config.settings import VECTOR_DB_PATH, EMBEDDING_MODEL, LLM_MODEL


# --------------------------------------------------
# Robust condition detection
# --------------------------------------------------
def detect_condition(question: str) -> Optional[str]:
    q = question.lower()

    diabetes_terms = [
        "diabetes",
        "diabetes mellitus",
        "mellitus",
        "milletus",
        "t2dm",
        "type 2 diabetes",
        "type ii diabetes",
        "dm",
    ]

    hypertension_terms = [
        "hypertension",
        "high blood pressure",
        "htn",
    ]

    for term in diabetes_terms:
        if term in q:
            return "diabetes"

    for term in hypertension_terms:
        if term in q:
            return "hypertension"

    return None


# --------------------------------------------------
# Main RAG logic
# --------------------------------------------------
def ask_guidelines(question: str) -> dict:
    condition = detect_condition(question)

    if not condition:
        return {
            "answer": (
                "I do not know. The condition in the question could not be identified."
            ),
            "sources": [],
        }

    index_path = Path(VECTOR_DB_PATH) / condition

    if not index_path.exists():
        return {
            "answer": (
                f"I do not know. No guidelines are available for condition: {condition}."
            ),
            "sources": [],
        }

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        request_timeout=30,
    )

    db = FAISS.load_local(
        index_path,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    docs = db.similarity_search(question, k=6)

    if not docs:
        return {
            "answer": (
                "I do not know. The provided guidelines do not contain information "
                "to answer this question."
            ),
            "sources": [],
        }

    context = "\n\n".join(
        f"Source: {d.metadata.get('source', 'unknown')}\n{d.page_content}"
        for d in docs
    )

    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=0,
        request_timeout=30,
    )

    prompt = f"""
You are a clinical decision support assistant.

Answer the question ONLY using the guideline context below.
If the answer is not explicitly stated in the context, say "I do not know".

Guideline context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    sources = sorted(
        {d.metadata.get("source", "unknown") for d in docs}
    )

    return {
        "answer": response.content,
        "sources": sources,
    }
