"""Text embeddings for the RAG notebooks: Voyage models through OpenRouter's embeddings endpoint.

The course uses the voyageai package with its own VOYAGE_API_KEY. OpenRouter serves the same
Voyage models, so the OpenRouter key from .env (ANTHROPIC_API_KEY) is enough.
"""

import os

import httpx
from dotenv import load_dotenv

load_dotenv()
EMBEDDINGS_URL = os.environ.get("ANTHROPIC_BASE_URL", "https://openrouter.ai/api") + "/v1/embeddings"


def generate_embedding(chunks, model="voyageai/voyage-4-large", input_type="query"):
    """Embed one text (returns one vector) or a list of texts (returns a list of vectors).

    input_type: "query" for questions, "document" for the chunks being searched.
    """
    is_list = isinstance(chunks, list)
    response = httpx.post(
        EMBEDDINGS_URL,
        headers={"Authorization": f"Bearer {os.environ['ANTHROPIC_API_KEY']}"},
        json={"model": model, "input": chunks if is_list else [chunks], "input_type": input_type},
        timeout=60,
    )
    response.raise_for_status()
    embeddings = [item["embedding"] for item in sorted(response.json()["data"], key=lambda item: item["index"])]
    return embeddings if is_list else embeddings[0]
