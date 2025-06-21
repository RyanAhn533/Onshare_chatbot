# utils/gpt_helper.py
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")  # 또는 st.secrets 사용

def ask_gpt(messages: list[dict]) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.3,
        max_tokens=400,
    )
    return response.choices[0].message.content.strip()
