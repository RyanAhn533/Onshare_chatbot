import streamlit as st
from utils.ui import multiselect_by_image, select_one_by_image, speak
from pathlib import Path

# ── 내장 페이지 전환 래퍼 ──────────────────────────────────────────────
def switch_page(page: str) -> None:
    """
    Streamlit 1.35+ 내장 st.switch_page() 사용.
    인수는 'pages/파일명.py' 형태이거나, 확장자·경로가 없으면 자동 보완.
    """
    if not page.endswith(".py"):
        page += ".py"
    if not page.startswith("pages/"):
        page = f"pages/{page}"
    st.switch_page(page)
# ─────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="① 손 씻기 & 도구", page_icon="🍳")
speak("손을 씻었는지 먼저 알려 주시고, 사용할 도구 그림을 눌러 주세요.")

# ── 1) 손 씻음 여부 (단일 선택) ──
hand_imgs = {
    "손 깨끗해요": Path("data/hand/clean.png"),
    "손 더러워요": Path("data/hand/dirty.png"),
}
hand_status = select_one_by_image("손을 씻었나요?", hand_imgs)

# ── 2) 준비된 도구 (다중 선택) ──
tool_imgs = {p.stem: p for p in Path("data/tools").glob("*.png")}
selected_tools = multiselect_by_image("사용할 도구를 골라 주세요", tool_imgs)

# ── 3) 진행·뒤로 버튼 ──
col1, col2, _ = st.columns([1, 1, 4])

with col1:
    if st.button("뒤로 ⬅️"):
        st.experimental_rerun()

with col2:
    if st.button("다음 단계 ➡️"):
        if hand_status is None:
            speak("손 씻기를 먼저 선택해 주세요.")
            st.warning("손 씻기 여부를 선택해 주세요.")
        elif hand_status == "손 더러워요":
            speak("먼저 손을 깨끗이 씻고 다시 눌러 주세요!")
            st.warning("⚠️ 손을 씻고 돌아오면 ‘다음 단계’ 버튼을 다시 눌러 주세요.")
        else:
            st.session_state["hand_status"] = hand_status
            st.session_state["selected_tools"] = selected_tools or ["없음"]
            switch_page("1_Ingredients")  # pages/1_Ingredients.py 로 이동
