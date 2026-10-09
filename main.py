import os
import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY가 없습니다.")


client = OpenAI()

MODEL = "gpt-6-luna"


# --------------------------------------------------
# 실제 Python 함수
# --------------------------------------------------

def get_weather(location):

    fake_weather_data = {
        "서울": {
            "temperature": 21,
            "condition": "맑음"
        },
        "인천": {
            "temperature": 20,
            "condition": "흐림"
        },
        "부산": {
            "temperature": 24,
            "condition": "맑음"
        }
    }

    weather = fake_weather_data.get(
        location,
        {
            "temperature": None,
            "condition": "정보 없음"
        }
    )

    return weather

def calculate(a, b, operation):

    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if operation == "divide":
        return a / b
# --------------------------------------------------
# AI에게 알려줄 Tool 정의
# --------------------------------------------------

tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "특정 도시의 현재 날씨 정보를 조회합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "날씨를 조회할 도시 이름"
                }
            },
            "required": ["location"],
            "additionalProperties": False
        },
        "strict": True
    },

    {
    "type": "function",
    "name": "calculate",
    "description": "두 숫자를 계산합니다.",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {
                "type": "number"
            },
            "b": {
                "type": "number"
            },
            "operation": {
                "type": "string",
                "enum": [
                    "add",
                    "subtract",
                    "multiply",
                    "divide"
                ]
            }
        },
        "required": [
            "a",
            "b",
            "operation"
        ],
        "additionalProperties": False
    },
    "strict": True
}
]


print("AI Tool Assistant")
print("종료하려면 exit 입력")


while True:

    user_input = input("\nYou: ").strip()

    if user_input.lower() == "exit":
        break

    if not user_input:
        continue

    # --------------------------------------------------
    # 1차 AI 요청
    # --------------------------------------------------

    response = client.responses.create(
        model=MODEL,
        input=user_input,
        tools=tools,
    )

    tool_used = False

    # --------------------------------------------------
    # AI가 Tool 호출을 요청했는지 확인
    # --------------------------------------------------

    for item in response.output:

        if item.type == "function_call":

            tool_used = True

            function_name = item.name

            print("선택된 tool:", function_name)

            arguments = json.loads(
                item.arguments
            )

            # --------------------------------------------------
            # 실제 함수 실행
            # --------------------------------------------------

            if function_name == "get_weather":

                result = get_weather(
                    arguments["location"]
                )

            elif function_name == "calculate":

                result = calculate(
                    arguments["a"],
                    arguments["b"],
                    arguments["operation"]
                )

                # --------------------------------------------------
                # 함수 결과를 다시 AI에게 전달
                # --------------------------------------------------

                final_response = client.responses.create(
                    model=MODEL,
                    previous_response_id=response.id,
                    input=[
                        {
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": json.dumps(
                                result,
                                ensure_ascii=False
                            )
                        }
                    ],
                    tools=tools,
                )

                print(
                    "\nAI:",
                    final_response.output_text
                )

    # Tool이 필요 없는 일반 질문
    if not tool_used:
        print("\nAI:", response.output_text)