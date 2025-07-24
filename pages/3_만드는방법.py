from pathlib import Path
import re
from PIL import Image
import streamlit as st

from utils.ui import speak, aac_control_panel
from recipe_templates import BASE_RECIPES  # 저장된 전체 레시피

# ── 페이지 설정 ──────────────────────────────────────────
st.set_page_config(page_title="④ 요리 도우미", page_icon="👩‍🍳")

# ── 세션 정보 가져오기 ───────────────────────────────────
menu: str | None = st.session_state.get("menu")
ingredients: list[str] = st.session_state.get("selected_ingredients", [])
tools: list[str] = st.session_state.get("selected_tools", [])
hand: str = st.session_state.get("hand_status", "깨끗해요")

if not menu:
    st.error("추천된 메뉴 정보가 없어요. 이전 단계로 돌아가 주세요.")
    st.stop()

# ── 유틸 상수 및 헬퍼 ───────────────────────────────────
MAX_STEPS = 15
MAX_STEP_LEN = 60
EASY_MAP = {"살모넬라": "식중독균", "캄필로박터": "식중독균"}
STEP_PREFIX_RE = re.compile(r"^\s*[①-⓯\d\\(\)]\s*")

def _apply_easy_words(text: str) -> str:
    for hard, easy in EASY_MAP.items():
        text = text.replace(hard, easy)
    return text

def _sanitize_for_tts(text: str) -> str:
    circled = "①②③④⑤⑥⑦⑧⑨⑩⓫⓬⓭⓮⓯"
    for i, ch in enumerate(circled, 1):
        text = text.replace(ch, f"{i}단계 ")
    return text

# ── 레시피 불러오기 및 세션 저장 ────────────────────────
def fetch_recipe() -> None:
    recipe = BASE_RECIPES.get(menu, {})
    steps = recipe.get("순서", [])

    if not steps:
        st.error(f"'{menu}' 메뉴의 레시피가 등록되어 있지 않습니다.")
        return

    clean_steps = []
    for line in steps:
        line = STEP_PREFIX_RE.sub("", line.strip())
        line = _apply_easy_words(line)
        clean_steps.append(line[:MAX_STEP_LEN])
    clean_steps = clean_steps[:MAX_STEPS]

    st.session_state.update({
        "recipe_steps": clean_steps,
        "step_idx": 0,
        "_spoken_idx": None,
    })

    # 메뉴 이미지 표시
    menu_img_path = Path("data/menu") / f"{menu}.png"
    if menu_img_path.exists():
        st.image(Image.open(menu_img_path), caption=f"추천 메뉴: {menu}", use_column_width=True)
    else:
        st.warning(f"'{menu}' 메뉴의 이미지를 찾을 수 없습니다.")

# ── 현재 단계 표시 ──────────────────────────────────────
def show_current_step() -> None:
    idx = st.session_state.get("step_idx", 0)
    steps = st.session_state.get("recipe_steps", [])

    if not steps:
        st.info("‘시작’ 버튼을 눌러 요리를 시작해 주세요.")
        return

    if idx >= len(steps):
        st.success("모든 단계가 끝났어요! 맛있게 드세요 😊")
        speak("모든 단계가 끝났어요! 맛있게 드세요.")
        return

    html = f"""
    <div style='background:#fff3cd;padding:12px;border-radius:8px;'>
        <b>{idx + 1}/{len(steps)}단계</b><br>{steps[idx]}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

    if st.session_state.get("_spoken_idx") != idx:
        speak(_sanitize_for_tts(steps[idx]))
        st.session_state["_spoken_idx"] = idx

# ── 버튼 콜백 ────────────────────────────────────────────
def on_start(_):
    fetch_recipe()
    show_current_step()

def on_next(_):
    if "recipe_steps" in st.session_state:
        if st.session_state["step_idx"] + 1 < len(st.session_state["recipe_steps"]):
            st.session_state["step_idx"] += 1
    show_current_step()

def on_prev(_):
    if "recipe_steps" in st.session_state:
        if st.session_state["step_idx"] > 0:
            st.session_state["step_idx"] -= 1
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
    "이전": (Path("data/aac_controls/back.png"), on_prev),
    "다시": (Path("data/aac_controls/again.png"), on_again),
    "그만": (Path("data/aac_controls/stop.png"), on_stop),
}

aac_control_panel(
    {label: (img, label) for label, (img, _) in controls.items()},
    lambda label: controls[label][1](label)
)

# ── 초기 화면 출력 ──────────────────────────────────────
if "recipe_steps" not in st.session_state:
    show_current_step()
