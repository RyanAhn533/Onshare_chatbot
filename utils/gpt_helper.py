from __future__ import annotations

import os
from typing import List, Dict
from openai import OpenAI

# ── 로컬 환경에서만 .env 로드 ─────────────────────────────
# .env에 OPENAI_API_KEY=sk-... 와 ENV=LOCAL 등이 들어 있음
if os.getenv("ENV", "LOCAL") == "LOCAL":
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # 배포 환경에서 dotenv 없어도 무시

# ── API 키 불러오기 ─────────────────────────────────────
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("❌ OPENAI_API_KEY가 설정되어 있지 않습니다. .env 또는 환경변수를 확인하세요.")

client = OpenAI(api_key=api_key)


def ask_gpt(messages: List[Dict[str, str]],
            model: str = "gpt-4o",
            temperature: float = 0.3,
            max_tokens: int = 400) -> str:
    """
    OpenAI Chat API 호출 → 응답 텍스트 반환
    """
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content.strip()
