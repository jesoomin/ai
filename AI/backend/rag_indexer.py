from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# 벡터스토어 불러오기
db = FAISS.load_local(index_path, OpenAIEmbeddings(...))

def search(query: str):
    retrieved_docs = db.similarity_search(query, k=3)  # Top 3 chunk 검색
    results = [
        {"metadata": doc.metadata, "page_content": doc.page_content}
        for doc in retrieved_docs
    ]
    if not results:
        # fallback logic
        return [{"metadata": {"location": query}, "page_content": "검색 결과 없음"}]
    return results