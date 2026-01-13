from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.config.settings import LLM_MODEL
from app.rag.prompt import SYSTEM_PROMPT
from app.rag.retriever import get_vector_db

llm = ChatOpenAI(
    model=LLM_MODEL,
    temperature=0
)

def ask_guidelines(question: str):
    db = get_vector_db()

    docs = db.similarity_search(question, k=4)

    if not docs:
        return {
            "answer": "Not found in the provided clinical guidelines.",
            "sources": []
        }

    context = "\n\n".join(d.page_content for d in docs)

    sources = sorted(
        {d.metadata.get("source", "unknown") for d in docs}
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"""
Context:
{context}

Question:
{question}
""")
    ]

    response = llm(messages)

    return {
        "answer": response.content,
        "sources": sources
    }
