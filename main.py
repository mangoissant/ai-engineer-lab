import os

from dotenv import load_dotenv
from openai import OpenAI


# .env 파일 읽기
load_dotenv()


# API key 확인
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY가 없습니다.")


# OpenAI 클라이언트 생성
client = OpenAI()

MODEL = "gpt-6-luna"


print("AI Assistant")
print("종료하려면 exit 입력")


while True:

    user_input = input("\nYou: ").strip()

    if user_input.lower() == "exit":
        print("종료합니다.")
        break

    if not user_input:
        continue

    try:

        response = client.responses.create(
            model=MODEL,
            instructions=(
                "You are an AI startup mentor. "
                "Answer in Korean. "
                "Be concise and always give one practical example."
            ),
            input=user_input,
        )

        print("\nAI:", response.output_text)

    except Exception as error:

        print("\nERROR:", error)