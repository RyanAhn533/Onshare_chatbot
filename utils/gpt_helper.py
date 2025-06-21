# utils/gpt_helper.py
"""
OpenAI Python SDK v1.x 버전에 맞춘 헬퍼 모듈
------------------------------------------------
* 사용법
    from utils.gpt_helper import ask_gpt
    answer = ask_gpt([
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ])
"""

from __future__ import annotations  # 타입 힌트 forward-ref (Py3.7+)

import os
from typing import List, Dict

from openai import OpenAI   # ⭐ v1 클라이언트

# 환경변수(또는 st.secrets)에서 API 키 읽기
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_gpt(messages: List[Dict[str, str]],
            model: str = "gpt-3.5-turbo",
            temperature: float = 0.3,
            max_tokens: int = 400) -> str:
    """
    ChatCompletion 한 번 호출하고 응답 문자열만 반환한다.

    Parameters
    ----------
    messages : list[dict]
        OpenAI chat 형식 메시지 배열
    model : str, optional
        사용할 모델 ID
    temperature : float, optional
        창의성(0.0‒2.0)
    max_tokens : int, optional
        생성될 최대 토큰 수

    Returns
    -------
    str
        모델이 생성한 메시지(content) 텍스트
    """
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content.strip()
