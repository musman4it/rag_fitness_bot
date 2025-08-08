import os
from dotenv import load_dotenv
import google.generativeai as genai
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

load_dotenv()

# Configure Gemini Flash
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
llm = genai.GenerativeModel("gemini-1.5-flash")

# Qdrant Cloud setup
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
COLLECTION_NAME = "fitness_docs"

# Embedding model (must match the one used for indexing)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_context(query, top_k=3):
    q_vec = embed_model.encode([query])[0].tolist()
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=q_vec,
        limit=top_k
    )
    context_pieces = [hit.payload["text"] for hit in hits]
    return "\n\n".join(context_pieces)

def get_answer(query):
    context = retrieve_context(query)
    prompt = f"""You are a helpful health & fitness coach. Use the context below to answer the user query.

Context:
{context}

Question: {query}

Answer concisely and practically:"""

    response = llm.generate_content(prompt)
    return response.text
