import os
import uuid
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer

load_dotenv()

# Qdrant Cloud client
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = "fitness_docs"

# Use a lightweight embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Recreate collection (overwrites if exists)
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=embed_model.get_sentence_embedding_dimension(), distance=Distance.COSINE),
)

def chunk_text(text, chunk_size=500):
    # naive splitting by characters; you can improve with sentence or token-aware chunking
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

def load_and_index():
    all_chunks = []
    for fname in os.listdir("data"):
        if not fname.endswith(".md"):
            continue
        with open(os.path.join("data", fname), encoding="utf-8") as f:
            content = f.read()
        chunks = chunk_text(content)
        for chunk in chunks:
            all_chunks.append(chunk)

    embeddings = embed_model.encode(all_chunks, show_progress_bar=True)
    points = []
    for chunk, vector in zip(all_chunks, embeddings):
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector.tolist(),
            payload={"text": chunk}
        ))

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Indexed {len(points)} chunks into Qdrant.")

if __name__ == "__main__":
    load_and_index()
