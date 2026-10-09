import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel


# --------------------------------------------------
# 환경 설정
# --------------------------------------------------

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY가 없습니다.")

client = OpenAI()

# Day 1, 2에서 정상 작동했던 모델명을 그대로 사용
MODEL = "gpt-6-luna"


# --------------------------------------------------
# AI가 출력해야 할 데이터 구조
# --------------------------------------------------

class TaskAnalysis(BaseModel):
    category: str
    priority: str
    summary: str
    action_items: list[str]
    estimated_minutes: int


# --------------------------------------------------
# 프로그램
# --------------------------------------------------

print("AI Task Analyzer")
print("종료하려면 exit 입력")


while True:

    user_input = input("\n할 일을 입력하세요: ").strip()

    if user_input.lower() == "exit":
        break

    if not user_input:
        continue

    try:

        response = client.responses.parse(
            model=MODEL,
            instructions=(
                "사용자의 요청을 할 일로 분석하세요. "
                "category는 work, study, personal 중 하나를 사용하세요. "
                "priority는 high, medium, low 중 하나를 사용하세요. "
                "summary는 짧고 명확한 한국어로 작성하세요."
            ),
            input=user_input,
            text_format=TaskAnalysis,
        )

        result = response.output_parsed

        print("\n--- AI 분석 결과 ---")
        print("Category:", result.category)
        print("Priority:", result.priority)
        if result.priority == "high":
            print("⚠️ 우선 처리해야 하는 작업입니다.")
        print("Summary:", result.summary)
        print("Estimated Time:", result.estimated_minutes, "minutes")
        print("Action Items:")

        for item in result.action_items:
            print("-", item)

    except Exception as error:

        print("\nERROR:", error)