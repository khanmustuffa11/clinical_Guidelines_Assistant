import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "vectordb/chroma")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in environment")
