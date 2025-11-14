from typing import List
from app_config import Config


def get_embedding(text: str) -> List[float]:
    """
    문자열 하나의 임베딩 반환 (동기 호출)
    AOAI/OpenAI가 설정되어 있으면 사용하고, 아니면 local sentence-transformers 모델 사용.
    """
    if Config.use_azure() or Config.use_openai():
        # OpenAI / AOAI 임베딩 사용
        try:
            import openai

            if Config.use_azure():
                openai.api_type = "azure"
                openai.api_base = Config.AOAI_ENDPOINT
                openai.api_version = "2024-10-01"
                openai.api_key = Config.AOAI_API_KEY
                model = Config.AOAI_DEPLOY_EMBED_3_LARGE or "text-embedding-3-large"
                # Azure uses `engine` param depending on SDK version; using `model` for compatibility
                resp = openai.Embedding.create(model=model, input=text)
            else:
                openai.api_key = Config.OPENAI_API_KEY
                resp = openai.Embedding.create(model="text-embedding-3-small", input=text)

            return resp["data"][0]["embedding"]
        except Exception as e:
            print("OpenAI embedding failed, falling back to local model:", e)

    # fallback: sentence-transformers
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    emb = model.encode(text).tolist()
    return emb


def get_embeddings(texts: List[str]) -> List[List[float]]:
    return [get_embedding(t) for t in texts]
