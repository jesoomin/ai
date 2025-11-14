import streamlit as st
from planner_agent import plan_trip

st.set_page_config(page_title="AI 여행 플래너", page_icon="🌍")
st.title("🌍 AI 여행 플래너 (로컬 문서 + Azure GPT)")

query = st.text_input("여행 목적이나 지역을 입력하세요:", "paris")

if st.button("플랜 생성"):
    with st.spinner("여행 계획 생성 중..."):
        try:
            result = plan_trip(query)
            if "error" in result:
                st.error(result["error"])
            else:
                st.subheader("🗺️ 여행 요약")
                st.write(result["summary"])
                st.subheader("📍 목적지")
                st.write(result["destination"])
                st.subheader("✅ 예약 정보")
                st.json(result["booking"])
        except Exception as e:
            st.error(f"오류 발생: {e}")
