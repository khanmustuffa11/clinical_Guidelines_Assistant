import os
from pathlib import Path

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunking import chunk_documents
from app.config.settings import VECTOR_DB_PATH, EMBEDDING_MODEL

# ✅ Resolve project root reliably
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "guidelines"



def ingest_guidelines(data_dir=DATA_DIR):
    print("📍 Using data directory:", data_dir)

    all_chunks = []

    if not data_dir.exists():
        raise RuntimeError(f"Guidelines directory not found: {data_dir}")

    for root, _, files in os.walk(data_dir):
        print("📂 Scanning:", root)
        for file in files:
            print("📄 Found file:", file)
            if file.lower().endswith(".pdf"):
                pdf_path = Path(root) / file
                print("➡️ Ingesting:", pdf_path)

                docs = load_pdf(str(pdf_path))
                chunks = chunk_documents(docs)

                for c in chunks:
                    c.metadata["source"] = str(pdf_path)

                all_chunks.extend(chunks)

    if not all_chunks:
        raise RuntimeError("No guideline documents found")

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    db = Chroma.from_documents(
        documents=all_chunks,
        embedding=embeddings,
        persist_directory=str(VECTOR_DB_PATH),
    )

    db.persist()

    num_sources = len({c.metadata.get("source") for c in all_chunks})

    print(
        f"✅ Ingested {len(all_chunks)} chunks "
        f"from {num_sources} guideline files"
    )


if __name__ == "__main__":
    ingest_guidelines()
