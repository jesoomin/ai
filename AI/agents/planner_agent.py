from typing import Optional, Dict, Any
from vector_store.faiss_store import FaissStore
from agents.rag_agent import RAGAgent


class PlannerAgent:
    def __init__(self, store_dir: Optional[str] = None):
        # 차별화 포인트: 사용자의 "여행 성향 프로필"을 유지하여 추천에 반영
        self.vs = FaissStore(path=store_dir)
        self.rag = RAGAgent(self.vs)

    def ingest_destination_docs(self, docs: Dict[str, str]):
        # docs: {id: markdown_text}
        for id, text in docs.items():
            self.vs.add(id, text, metadata={"source": "user_upload"})

    def recommend(self, query: str, profile: Dict[str, Any] = None) -> str:
        # profile: {'travel_style': 'relax'/'adventure', 'budget': 'low'/'mid'/'high', 'days': 2}
        # profile를 prompt에 넣어 RAG Agent에 전달
        pref_str = ""
        if profile:
            pref_str = f"사용자 성향: {profile}\n"
        augmented_query = pref_str + query
        return self.rag.answer(augmented_query)
