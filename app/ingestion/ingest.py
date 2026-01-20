import os
from pathlib import Path
from collections import defaultdict

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunking import chunk_documents
from app.config.settings import DATA_DIR, VECTOR_DB_PATH, EMBEDDING_MODEL


def ingest_guidelines():
    data_dir = Path(DATA_DIR)
    vector_root = Path(VECTOR_DB_PATH)

    print(f"📍 Using data directory: {data_dir}")

    if not data_dir.exists():
        raise RuntimeError(f"Guidelines directory not found: {data_dir}")

    # Group chunks by condition
    condition_chunks = defaultdict(list)

    for root, _, files in os.walk(data_dir):
        for file in files:
            if not file.lower().endswith(".pdf"):
                continue

            pdf_path = Path(root) / file
            condition = pdf_path.parent.name.lower()

            print(f"➡️ Ingesting {pdf_path} (condition={condition})")

            docs = load_pdf(pdf_path)

            # Attach metadata BEFORE chunking
            for d in docs:
                d.metadata["source"] = str(pdf_path)
                d.metadata["condition"] = condition

            chunks = chunk_documents(docs)

            if not chunks:
                print(f"⚠️ No chunks created for {pdf_path} — skipping")
                continue

            print(f"   ✂️ Created {len(chunks)} chunks")
            condition_chunks[condition].extend(chunks)

    if not condition_chunks:
        raise RuntimeError("No chunks were created from any guideline documents")

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        request_timeout=30,
    )

    vector_root.mkdir(parents=True, exist_ok=True)

    for condition, chunks in condition_chunks.items():
        if not chunks:
            print(f"⚠️ Skipping condition '{condition}' — no chunks")
            continue

        print(f"📦 Building FAISS index for condition: {condition}")
        print(f"   📊 Total chunks: {len(chunks)}")

        db = FAISS.from_documents(chunks, embeddings)

        condition_path = vector_root / condition
        condition_path.mkdir(parents=True, exist_ok=True)

        db.save_local(condition_path)

        print(f"✅ Saved FAISS index for '{condition}'")

    print("🎉 Ingestion completed successfully for all conditions")


if __name__ == "__main__":
    ingest_guidelines()
