from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def chunk_documents(
    documents: list[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> list[Document]:
    """
    Robust chunking that NEVER silently drops valid text.
    Compatible with modern LangChain versions.
    """

    if not documents:
        return []

    # Keep only documents with real text
    valid_docs = []
    for d in documents:
        text = (d.page_content or "").strip()
        if text:
            valid_docs.append(d)

    if not valid_docs:
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ],
    )

    chunks = splitter.split_documents(valid_docs)

    # 🔒 Fallback: if splitter fails but text exists
    if not chunks:
        fallback_chunks = []
        for d in valid_docs:
            fallback_chunks.append(
                Document(
                    page_content=d.page_content,
                    metadata=d.metadata,
                )
            )
        return fallback_chunks

    return chunks
