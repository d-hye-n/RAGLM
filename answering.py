import os
from google import genai
from google.genai import types

MODEL_NAME = "gemini-3.1-flash-lite-preview"

def build_context(results):
    context_parts = []
    for result in results:
        context_parts.append(
            f"[page {result['page']}]\n{result['text']}"
        )

    return "\n\n".join(context_parts)

def answer_question(question, context, api_key):
    if not api_key:
        return "GEMINI API KEY is not setting"

    if not question.strip():
        return "Question is empty"

    if not context.strip():
        return "No context searched"

    client = genai.Client(api_key=api_key)

    prompt = f"""아래 문맥만 근거로 질문에 답하세요.
    문맥에 없는 내용은 추측하지 말고, 문맥에 없다고 말하세요.
    입력받은 언어로 대답하세요.
    질문:
    {question}
    문맥:
    {context}

    답변 형식:
    1. 먼저 간단히 답변
    2. 그 다음 핵심 근거를 짧게 정리"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="당신은 PDF 문서를 기반으로 답변하는 어시스턴트입니다. 근거 없는 추측은 하지 마세요.",
            temperature=0.2,
            max_output_tokens=512,
            thinking_config=types.ThinkingConfig(
                thinking_level="minimal"
            ),
        ),
    )

    return response.text or "No response"
