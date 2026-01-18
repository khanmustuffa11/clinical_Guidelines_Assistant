import os
from pathlib import Path

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunking import chunk_documents
from app.config.settings import (
    DATA_DIR,
    VECTOR_DB_PATH,
    EMBEDDING_MODEL,
)

def ingest_guidelines():
    data_dir = Path(DATA_DIR)

    print(f"📍 Using data directory: {data_dir}")

    if not data_dir.exists():
        raise RuntimeError(f"Guidelines directory not found: {data_dir}")

    all_chunks = []
    pdf_count = 0

    for root, _, files in os.walk(data_dir):
        print(f"📂 Scanning: {root}")
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = Path(root) / file
                print(f"➡️ Ingesting: {pdf_path}")

                docs = load_pdf(pdf_path)
                chunks = chunk_documents(docs)

                all_chunks.extend(chunks)
                pdf_count += 1

    if not all_chunks:
        raise RuntimeError("No guideline documents found")

    print(f"🧠 Creating embeddings using model: {EMBEDDING_MODEL}")

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        request_timeout=30,
    )

    print("📦 Building FAISS vector store")
    db = FAISS.from_documents(all_chunks, embeddings)

    vector_db_path = Path(VECTOR_DB_PATH)
    vector_db_path.mkdir(parents=True, exist_ok=True)

    db.save_local(vector_db_path)

    unique_sources = {c.metadata.get("source") for c in all_chunks}

    print(
        f"✅ Ingested {len(all_chunks)} chunks "
        f"from {len(unique_sources)} guideline files"
    )

if __name__ == "__main__":
    ingest_guidelines()
