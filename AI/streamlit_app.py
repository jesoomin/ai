import streamlit as st
from app_config import Config
from agents.planner_agent import PlannerAgent
import os

st.set_page_config(page_title="AI 여행 플래너 전문가", layout="wide")

st.title("AI 여행 플래너 전문가 ✈️")

# 초기화
planner = PlannerAgent(store_dir=Config.VECTOR_STORE_DIR)

with st.sidebar:
    st.header("설정")
    days = st.slider("여행 일수", 1, 14, 3)
    travel_style = st.selectbox("여행 성향", ["relax", "adventure", "culture", "family"])
    budget = st.selectbox("예산 수준", ["low", "mid", "high"])
    api_mode = st.radio("LLM 모드", ["OpenAI/AOAI (환경변수 필요)", "로컬(임베딩만)"])
    st.markdown("---")
    st.caption("환경변수 및 AOAI 키를 설정하면 AOAI/OpenAI로 연결됩니다.")

st.markdown("---")
st.header("질문 또는 요청 입력")
user_query = st.text_area("예: 서울에서 2박3일 가족 여행 추천 일정과 교통편을 알려줘", height=120)

if st.button("추천 생성"):
    if not user_query.strip():
        st.warning("질문을 입력해주세요.")
    else:
        profile = {"days": days, "travel_style": travel_style, "budget": budget}
        with st.spinner("추천 생성 중... (RAG 검색 및 LLM 호출) "):
            resp = planner.recommend(user_query, profile=profile)
        st.subheader("추천 결과")
        st.write(resp)

st.markdown("---")
st.header("데이터 업로드 (RAG용)")
uploaded = st.file_uploader("여행지 문서 업로드 (Markdown / TXT)", accept_multiple_files=True)
if uploaded:
    docs = {}
    for f in uploaded:
        text = f.read().decode("utf-8")
        docs[f.name] = text
    planner.ingest_destination_docs(docs)
    st.success(f"{len(docs)}개 문서를 벡터스토어에 저장했습니다.")