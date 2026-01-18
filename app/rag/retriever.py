from pathlib import Path

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.config.settings import VECTOR_DB_PATH, EMBEDDING_MODEL


def get_vector_db():
    vector_db_path = Path(VECTOR_DB_PATH)

    if not vector_db_path.exists():
        raise RuntimeError(
            f"Vector DB not found at {vector_db_path}. "
            f"Run ingestion first."
        )

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        request_timeout=30,
    )

    # ⚠️ allow_dangerous_deserialization is REQUIRED for FAISS on Windows
    db = FAISS.load_local(
        vector_db_path,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    return db
