from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path

def load_pdf(pdf_path: str):
    if not Path(pdf_path).exists():
        raise FileNotFoundError(f"{pdf_path} not found")

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return documents
