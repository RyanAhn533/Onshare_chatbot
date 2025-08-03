from pathlib import Path
import re
from PIL import Image
import streamlit as st

from utils.ui import speak, aac_control_panel
from utils.gpt_helper import ask_gpt

# ── 페이지 설정 ─────────────────────────────
st.set_page_config(page_title="④ 요리 도우미", page_icon="👩‍🍳")

# ── 세션 정보 가져오기 ─────────────────────
menu        = st.session_state.get("menu")
ingredients = st.session_state.get("selected_ingredients", [])
tools       = st.session_state.get("selected_tools", [])
hand        = st.session_state.get("hand_status", "깨끗해요")
gpt_text    = st.session_state.get("gpt_response")

if not all([menu, gpt_text]):
    st.error("이전 단계 정보가 없습니다. 처음부터 다시 진행해 주세요.")
    st.stop()

# ── 레시피 추출 관련 상수 ─────────────────
MAX_STEPS = 15
MAX_STEP_LEN = 60
EASY_MAP = {"살모넬라": "식중독균", "캄필로박터": "식중독균"}
STEP_PREFIX_RE = re.compile(r"^\s*[①-⓯\d\\(\)]\s*")

# ── 텍스트 정제 함수들 ─────────────────────
def _apply_easy_words(text: str) -> str:
    for hard, easy in EASY_MAP.items():
        text = text.replace(hard, easy)
    return text

def _sanitize_for_tts(text: str) -> str:
    circled = "①②③④⑤⑥⑦⑧⑨⑩⓫⓬⓭⓮⓯"
    for i, ch in enumerate(circled, 1):
        text = text.replace(ch, f"{i}단계 ")
    return text

# ── GPT 응답에서 조리 단계만 추출 ─────────
def extract_steps_from_gpt(text: str) -> list[str]:
    step_pattern = re.compile(r"^\s*\d+[).]?\s+(.*)", re.MULTILINE)
    steps = step_pattern.findall(text)
    if not steps:
        steps = [text]
    clean_steps = []
    for line in steps:
        line = STEP_PREFIX_RE.sub("", line.strip())
        line = _apply_easy_words(line)
        clean_steps.append(line[:MAX_STEP_LEN])
    return clean_steps[:MAX_STEPS]

# ── 레시피 세션에 저장 및 메뉴 이미지 출력 ─
def fetch_recipe():
    steps = extract_steps_from_gpt(gpt_text)

    st.session_state.update({
        "recipe_steps": steps,
        "step_idx": 0,
        "_spoken_idx": None,
    })

    menu_img_path = Path("data/menu") / f"{menu}.png"
    if menu_img_path.exists():
        st.image(Image.open(menu_img_path), caption=f"추천 메뉴: {menu}", use_container_width=True)
    else:
        st.warning(f"'{menu}' 메뉴의 이미지를 찾을 수 없습니다.")

# ── 현재 단계 표시 ─────────────────────────
def show_current_step():
    idx = st.session_state.get("step_idx", 0)
    steps = st.session_state.get("recipe_steps", [])

    if not steps:
        st.info("‘시작’ 버튼을 누르면 요리를 시작할 수 있어요.")
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

# ── 버튼 콜백 ───────────────────────────────
def on_start(_): fetch_recipe(); show_current_step()
def on_next(_): st.session_state["step_idx"] += 1; show_current_step()
def on_prev(_): st.session_state["step_idx"] -= 1; show_current_step()
def on_again(_): show_current_step()
def on_stop(_): st.session_state["step_idx"] = 1_000_000; show_current_step()

# ── AAC 버튼 이미지 + 동작 정의 ──────────────
controls = {
    "시작": ("start.png", on_start),
    "다음": ("next.png", on_next),
    "이전": ("back.png", on_prev),
    "다시": ("again.png", on_again),
    "그만": ("stop.png", on_stop),
}

# ── AAC 이미지 클릭 UI (image_select 기반) ──
from streamlit_image_select import image_select

st.write("#### 🎛 요리 제어 버튼을 선택하세요")
aac_imgs = {label: Path("data/aac_controls") / img for label, (img, _) in controls.items()}
selected = image_select(
    label="",
    images=[str(p) for p in aac_imgs.values()],
    captions=list(aac_imgs.keys()),
    use_container_width=True,
)

if selected:
    label = [k for k, v in aac_imgs.items() if str(v) == selected][0]
    speak(label)
    controls[label][1](label)

# ── 초기 상태 출력 ───────────────────────────
if "recipe_steps" not in st.session_state:
    show_current_step()
