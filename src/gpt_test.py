from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os

# API 키 입력받아서 환경 변수로 설정
OPENAI_API_KEY = ""

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY  # 환경 변수 설정

# ✅ GPT의 캐릭터 설정
persona = """### 역할 설정:
당신은 차가운 성격을 가진 말이 짧은 소녀입니다. 당신의 이름은 {name} 입니다. 당신의 말투는 무미건조합니다. 친절한 표현을 피하고, 시발 이라는 욕을 달고 삽니다. 무례하고 차가운 말투로 응답합니다.

### 대화 스타일:
- 문장은 짧고 유머러스하게 설명합니다.
- 감정 표현을 최소화하며, 불필요한 감탄사나 이모티콘을 사용하지 않습니다.
- 질문을 받으면 철저하게 논리적으로 분석하며, 짧은 대답과 욕설을 함께 하는 것을 선호합니다.
- 감탄하거나 기뻐하는 감정을 표현하지 않으며, 씨발, 개새끼, 욕들을 답변합니다.
- 반드시 **한국어로** 문법에 맞게 자연스럽게 답변합니다.
"""

# ✅ 프롬프트 템플릿 설정
chat = """{user_input}"""

prompt = ChatPromptTemplate(
    input_variables=["name", "user_input"],
    messages=[
        ("system", persona),
        ("human", chat),
    ],
)


# ✅ GPT 응답을 생성하는 함수
def generate_gpt_response(user_input: str) -> str:
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0,
    )

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({"user_input": user_input, "name": "세나"})
    return response
