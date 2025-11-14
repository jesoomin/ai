import os
from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model

if Config.use_azure():
    llm = init_chat_model(
        model="gpt-4o",
        model_provider="azure_openai",
        temperature=0,
        azure_endpoint=Config.AOAI_ENDPOINT,
        azure_deployment=Config.AOAI_DEPLOY_GPT4O,
        openai_api_key=Config.AOAI_API_KEY,
        openai_api_version="2024-10-01"
    )
else:
    llm = init_chat_model(
        model="gpt-4o",
        temperature=0,
        api_key=Config.OPENAI_API_KEY
    )


class Config:
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # AOAI (Azure OpenAI)
    AOAI_ENDPOINT = os.getenv("AOAI_ENDPOINT")
    AOAI_API_KEY = os.getenv("AOAI_API_KEY")
    AOAI_DEPLOY_GPT4O = os.getenv("AOAI_DEPLOY_GPT4O") or "gpt-4o"
    AOAI_DEPLOY_EMBED_3_LARGE = os.getenv("AOAI_DEPLOY_EMBED_3_LARGE") or "text-embedding-3-large"

    VECTOR_STORE_DIR = os.getenv("VECTOR_DB_DIR", "vector_store")

    @classmethod
    def use_azure(cls):
        return bool(cls.AOAI_ENDPOINT and cls.AOAI_API_KEY)

    @classmethod
    def use_openai(cls):
        return bool(cls.OPENAI_API_KEY)
