"""발달장애인 친화형 요리 도우미 페이지

- GPT 프롬프트에 WHO‧CDC 식품안전 CoT를 포함해 안전한 레시피 생성
- 번호 파싱을 정규식으로 보강해 모든 번호 형식을 지원
- 단계/문장 길이 제한으로 과도한 정보 방지
- 음성(TTS)에서 특수 번호를 읽기 쉬운 형태로 변환
- Easy word mapping으로 어려운 용어를 쉬운 단어로 치환
- UI: 현재 단계 하이라이트, Spinner, Index‑Error 방지 로직 강화
"""

from pathlib import Path
import re
import streamlit as st
from utils.ui import speak, aac_control_panel
from utils.gpt_helper import ask_gpt

# ── 스트림릿 기본 설정 ───────────────────────────────────
st.set_page_config(page_title="④ 요리 도우미", page_icon="👩‍🍳")

# ── 세션 데이터 가져오기 ─────────────────────────────────
menu: str | None = st.session_state.get("menu")
ingredients: list[str] | None = st.session_state.get("selected_ingredients")
tools: list[str] | None = st.session_state.get("selected_tools")
hand: str | None = st.session_state.get("hand_status")

if not all([menu, ingredients, tools, hand]):
    st.error("이전 단계 정보가 없어요. 처음부터 다시 진행해 주세요.")
    st.stop()

# ── 상수 및 헬퍼 ──────────────────────────────────────────
MAX_STEPS = 15           # 단계 수 제한
MAX_STEP_LEN = 60        # 한 문장 최대 길이(문자 수)

EASY_MAP = {
    "살모넬라": "식중독균",
    "캄필로박터": "식중독균",
}

STEP_PREFIX_RE = re.compile(r"^\s*[①-⓯\d\.\(\)]\s*")

def _apply_easy_words(text: str) -> str:
    for hard, easy in EASY_MAP.items():
        text = text.replace(hard, easy)
    return text

def _sanitize_for_tts(text: str) -> str:
    circled = "①②③④⑤⑥⑦⑧⑨⑩⓫⓬⓭⓮⓯"
    for i, ch in enumerate(circled, 1):
        text = text.replace(ch, f"{i}단계 ")
    return text

# ── 레시피 GPT 호출 ──────────────────────────────────────
def fetch_recipe() -> None:
    context = (
        f"손 상태: {hand}\n"
        f"도구: {', '.join(tools)}\n"
        f"재료: {', '.join(ingredients)}\n"
        f"메뉴: {menu}\n"
    )
    
    prompt = (
        context
        + "위 정보를 참고해, 발달장애인을 위한 쉬운 요리 단계를 만들어 주세요. "
          "총 15단계를 넘기지 말고, 가능한 한 가장 간단한 단계로 설명해 주세요. "
          "각 문장은 ①, ②처럼 번호만 붙이고, 각 문장의 길이는 60자 이내로 해 주세요. "
          "각 단계마다 재료의 **정확한 양**을 써 주세요. "
          "예: '고추장 아빠 숟가락 1개 넣어요', '마늘 2쪽 다져요'. "
          "다음과 같은 WHO 위생 수칙(CoT 형식으로)을 따르세요:\n"
          "- 손은 요리 전 20초 이상 씻어요 (Keep Clean)\n"
          "- 생재료와 익힌 재료는 따로 도구를 써요 (Separate Raw & Cooked)\n"
          "- 음식은 중심까지 익혀요, 중심온도계 써요 (Cook Thoroughly)\n"
          "- 익힌 음식은 바로 먹거나 2시간 안에 냉장해요 (Keep at Safe Temps)\n"
          "- 유통기한, 알레르기, 물의 안전을 확인해요 (Use Safe Water & Raw Materials)\n"
          "각 단계에서 해당되는 위생 수칙이 있다면 **자연스럽게 이유와 실천법을 설명해 주세요.** "
          "예: '닭은 생으로 만졌으면 손을 씻어요. 세균이 번질 수 있어요.' "
          "불필요한 인삿말 없이 요리 과정과 주의사항만 말해 주세요."
    )

    msgs = [
        {
            "role": "system",
            "content": (
                "당신은 발달장애 아동에게 요리를 가르치는 초등학교 선생님입니다. "
                "모든 문장은 짧고 쉽게, 한 단계씩 논리 흐름을 따라 설명하세요 (Chain-of-Thought). "
                "각 문장에는 반드시 재료의 양을 구체적으로 말해 주세요. "
                "위험하거나 주의할 점은 그 이유와 함께 쉽게 설명하고, '어떻게 하면 안전한지' 예를 들어 주세요. "
                "예: '칼을 쓸 땐 조심해요. 손이 다칠 수 있어요. 도마 위에서만 써요.' "
                "WHO와 CDC의 식품안전 5대 수칙(Five Keys to Safer Food)을 참고하여 적절한 단계에 자연스럽게 반영하세요. "
                "음식 안전을 지키면서도 요리를 즐길 수 있도록, 친절하고 따뜻한 말투로 설명하세요."
            ),
        },
        {"role": "user", "content": prompt},
    ]

    with st.spinner("레시피 생성 중..."):
        raw: str = ask_gpt(msgs)

    steps: list[str] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        line = STEP_PREFIX_RE.sub("", line.strip())
        line = _apply_easy_words(line)
        steps.append(line[:MAX_STEP_LEN])

    steps = steps[:MAX_STEPS]

    st.session_state.update({
        "recipe_steps": steps,
        "step_idx": 0,
        "_spoken_idx": None,
    })

# ── 단계 표시 ────────────────────────────────────────────
def show_current_step() -> None:
    idx: int = st.session_state.get("step_idx", 0)
    steps: list[str] = st.session_state.get("recipe_steps", [])

    if not steps:
        st.info("‘시작’ 버튼을 눌러 요리를 시작해 주세요.")
        return

    if idx >= len(steps):
        st.success("모든 단계가 끝났어요! 맛있게 드세요 😊")
        speak("모든 단계가 끝났어요! 맛있게 드세요.")
        return

    html = (
        f"<div style='background:#fff3cd;padding:12px;border-radius:8px;'>"
        f"<b>{idx + 1}/{len(steps)}단계</b><br>{steps[idx]}</div>"
    )
    st.markdown(html, unsafe_allow_html=True)

    if st.session_state.get("_spoken_idx") != idx:
        speak(_sanitize_for_tts(steps[idx]))
        st.session_state["_spoken_idx"] = idx

# ── 버튼 콜백 ────────────────────────────────────────────
def on_start(_):
    if "recipe_steps" not in st.session_state:
        fetch_recipe()
    show_current_step()

def on_next(_):
    if "recipe_steps" in st.session_state:
        if st.session_state["step_idx"] + 1 < len(st.session_state["recipe_steps"]):
            st.session_state["step_idx"] += 1
    show_current_step()

def on_again(_):
    show_current_step()

def on_stop(_):
    st.session_state["step_idx"] = 1_000_000
    show_current_step()

# ── AAC 버튼 세트 ───────────────────────────────────────
controls = {
    "시작": (Path("data/aac_controls/start.png"), on_start),
    "다음": (Path("data/aac_controls/next.png"), on_next),
    "다시": (Path("data/aac_controls/again.png"), on_again),
    "그만": (Path("data/aac_controls/stop.png"), on_stop),
}

aac_control_panel(
    {lbl: (img_path, lbl) for lbl, (img_path, _) in controls.items()},
    lambda lbl: controls[lbl][1](lbl),
)

# ── 초기 화면 ───────────────────────────────────────────
if "recipe_steps" not in st.session_state:
    show_current_step()
