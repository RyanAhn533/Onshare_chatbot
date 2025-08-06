from pathlib import Path
from PIL import Image
import streamlit as st
from utils.ui import speak
from base_recipes import BASE_RECIPES  # BASE_RECIPES 모듈 임포트

# ── 페이지 설정 ─────────────────────────────
st.set_page_config(page_title="④ 요리 도우미", page_icon="👩‍🍳")

# ── 세션 정보 가져오기 ─────────────────────
menu        = st.session_state.get("menu")
ingredients = st.session_state.get("selected_ingredients", [])
tools       = st.session_state.get("selected_tools", [])
hand        = st.session_state.get("hand_status", "깨끗해요")

if not menu:
    st.error("이전 단계 정보가 없습니다. 처음부터 다시 진행해 주세요.")
    st.stop()

# ── 텍스트 정제 함수 ─────────────────────
def _sanitize_for_tts(text: str) -> str:
    circled = "①②③④⑤⑥⑦⑧⑨⑩⓫⓬⓭⓮⓯"
    for i, ch in enumerate(circled, 1):
        text = text.replace(ch, f"{i}단계 ")
    return text

# ── 레시피 세션에 저장 및 메뉴 이미지 출력 ─
def fetch_recipe():
    if menu not in BASE_RECIPES:
        st.error(f"'{menu}' 메뉴의 레시피를 찾을 수 없습니다.")
        return

    steps = BASE_RECIPES[menu]['순서']  # BASE_RECIPES에서 직접 불러오기

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

    st.markdown(f"""
    <div style='background:#fff3cd;padding:12px;border-radius:8px;'>
        <b>{idx + 1}/{len(steps)}단계</b><br>{steps[idx]}
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("_spoken_idx") != idx:
        speak(_sanitize_for_tts(steps[idx]))
        st.session_state["_spoken_idx"] = idx

# ── 버튼 콜백 ───────────────────────────────
def on_start(): fetch_recipe(); show_current_step()
def on_next(): st.session_state["step_idx"] += 1; show_current_step()
def on_prev(): st.session_state["step_idx"] -= 1; show_current_step()
def on_again(): show_current_step()
def on_stop(): st.session_state["step_idx"] = 1_000_000; show_current_step()

# ── 메뉴 이미지 표시 ───────────────────────
menu_img_path = Path("data/menu") / f"{menu}.png"
if menu_img_path.exists():
    st.image(Image.open(menu_img_path), caption=f"추천 메뉴: {menu}", use_container_width=True)

# ── 버튼 한 줄 배치 ───────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
with col1: st.button("▶ 시작", on_click=on_start, use_container_width=True)
with col2: st.button("⏭ 다음", on_click=on_next, use_container_width=True)
with col3: st.button("⏮ 이전", on_click=on_prev, use_container_width=True)
with col4: st.button("🔄 다시", on_click=on_again, use_container_width=True)
with col5: st.button("⏹ 그만", on_click=on_stop, use_container_width=True)

# ── 현재 단계 표시 ─────────────────────────
show_current_step()

# ── 전체 단계 미리보기 ─────────────────────
if "recipe_steps" in st.session_state:
    st.markdown("### 📜 전체 조리 단계")
    for i, step in enumerate(st.session_state["recipe_steps"], 1):
        st.markdown(f"{i}. {step}")
