import hashlib
import pdfplumber
import chromadb
from chromadb.utils import embedding_functions

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

chroma_client = chromadb.PersistentClient(path="./chroma_db")
embedding_fn = embedding_functions.DefaultEmbeddingFunction()


def _chunk_text(text: str) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end].strip())
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return [c for c in chunks if c]


def pdf_to_collection(file_bytes: bytes, filename: str) -> str:
    file_hash = hashlib.md5(file_bytes).hexdigest()[:12]
    collection_name = f"pdf_{file_hash}"

    existing = [c.name for c in chroma_client.list_collections()]
    if collection_name in existing:
        return collection_name

    with pdfplumber.open(__import__("io").BytesIO(file_bytes)) as pdf:
        full_text = "\n".join(
            page.extract_text() or "" for page in pdf.pages
        )

    if not full_text.strip():
        raise ValueError("No extractable text found in the PDF.")

    chunks = _chunk_text(full_text)
    collection = chroma_client.create_collection(
        name=collection_name,
        embedding_function=embedding_fn,
        metadata={"filename": filename},
    )
    collection.add(
        documents=chunks,
        ids=[f"{collection_name}_{i}" for i in range(len(chunks))],
    )
    return collection_name


def query_collection(collection_name: str, question: str, n_results: int = 5) -> list[str]:
    collection = chroma_client.get_collection(
        name=collection_name,
        embedding_function=embedding_fn,
    )
    results = collection.query(query_texts=[question], n_results=n_results)
    return results["documents"][0]
