from langchain_openai import ChatOpenAI
from app.rag.retriever import get_vector_db
from app.config.settings import LLM_MODEL

def ask_guidelines(question: str) -> dict:
    # 1️⃣ Load vector DB
    db = get_vector_db()

    # 2️⃣ Retrieve documents (FAIL FAST)
    try:
        docs = db.similarity_search(question, k=4)
    except Exception as e:
        raise RuntimeError(f"Vector search failed: {e}")

    if not docs:
        return {
            "answer": "No relevant clinical guideline information was found.",
            "sources": []
        }

    # 3️⃣ Build context safely
    context = "\n\n".join(
        f"Source: {d.metadata.get('source', 'unknown')}\n{d.page_content}"
        for d in docs
    )

    # 4️⃣ Create LLM with timeout
    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=0,
        request_timeout=30
    )

    prompt = f"""
You are a clinical decision support assistant.
Answer ONLY using the provided guideline context.
If the answer is not present, say you do not know.

Context:
{context}

Question:
{question}
"""

    # 5️⃣ Call LLM (FAIL FAST)
    try:
        response = llm.invoke(prompt)
    except Exception as e:
        raise RuntimeError(f"LLM invocation failed: {e}")

    sources = sorted(
        {d.metadata.get("source", "unknown") for d in docs}
    )

    return {
        "answer": response.content,
        "sources": sources
    }
