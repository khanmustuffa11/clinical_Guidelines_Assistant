from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from app.config.settings import VECTOR_DB_PATH, EMBEDDING_MODEL

def get_vector_db():
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    db = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

    return db
