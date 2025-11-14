import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-05-01-preview"),
    temperature=0.7
)

DOCS_DIR = "./data/sample_guides"

# 프롬프트 템플릿 정의
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "당신은 여행 가이드입니다."),
    ("human", """{doc_content}

100~200자 내외로 핵심 관광지와 특징을 요약해 추천해 주세요.""")
])


def search(query: str):
    file_path = os.path.join(DOCS_DIR, f"{query.lower()}.txt")

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            doc_content = f.read()
    else:
        doc_content = f"여행지 '{query}'에 대한 로컬 문서가 없습니다. GPT 지식을 기반으로 요약해 주세요."

    prompt = prompt_template.invoke({"doc_content": doc_content})
    result = llm.invoke(prompt)
    content = result.content.strip()

    return [{"metadata": {"location": query}, "page_content": content}]