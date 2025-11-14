from typing import List
from app_config import Config
from agents.embeddings_provider import get_embedding
from vector_store.faiss_store import FaissStore
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# AOAI 전용 초기화
if Config.use_azure():
    llm = ChatOpenAI(
        model=Config.AOAI_DEPLOY_GPT4O or "gpt-4o",
        temperature=0,
        openai_api_base=Config.AOAI_ENDPOINT,
        openai_api_key=Config.AOAI_API_KEY,
        openai_api_type="azure",
        openai_api_version="2024-10-01"
    )
else:
    raise ValueError("AOAI 키가 설정되어 있지 않습니다. .env 확인 필요")


def call_llm(prompt):
    messages = [
        SystemMessage("You are a travel planner."),
        HumanMessage(prompt)
    ]
    return response.content
    


class RAGAgent:
    def __init__(self, vector_store: FaissStore):
        self.vs = vector_store

    def answer(self, user_query: str, top_k: int = 4) -> str:
        docs = self.vs.search(user_query, top_k=top_k)
        context = "\n---\n".join([f"(source id:{d['id']}) {d['text']}" for d in docs])
        prompt = (
            f"너는 여행 플래너 전문가입니다. 사용자의 질문에 친절하고 구체적으로 답하십시오.\n\n"
            f"[컨텍스트]\n{context}\n\n"
            f"[질문]\n{user_query}\n\n"
            f"[요구사항]\n- 추천 일정, 소요시간, 교통수단, 예상비용(대략), 추천 활동을 제시하세요.\n"
            f"- 필요하면 더 질문하세요."
        )
        resp = call_llm(prompt)
        return resp
