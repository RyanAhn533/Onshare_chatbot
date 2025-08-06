import streamlit as st
from utils.ui import multiselect_by_image, select_one_by_image, speak
from pathlib import Path

# ── Streamlit 1.35+ 내장 페이지 전환 래퍼 ──
def switch_page(page: str):
    if not page.endswith(".py"):
        page += ".py"
    if not page.startswith("pages/"):
        page = f"pages/{page}"
    st.switch_page(page)
# ────────────────────────────────────────────

st.set_page_config(page_title="① 손 씻기 & 도구", page_icon="🍳")

# ✅ 최상단 제목
st.markdown("<h1 style='text-align: center; margin-top: -40px;'>🍳 요리용 챗봇 온쿡</h1>", unsafe_allow_html=True)

speak("손을 씻었는지 먼저 알려 주시고, 사용할 도구 그림을 눌러 주세요.")

# ── 1) 손 씻음 여부 ──────────────────────────────────────
hand_imgs = {
    "손 깨끗해요": Path(r"C:\chat_bot_aac_final\data\hand\clean.png"),
    "손 더러워요": Path(r"C:\chat_bot_aac_final\data\hand\dirty.png"),
}
hand_status = select_one_by_image("손을 씻었나요?", hand_imgs)

# ── 2) 준비된 도구 ──────────────────────────────────────
base_path = r"C:\chat_bot_aac_final\data\tools"
tool_imgs = {
    "가스레인지": f"{base_path}\\가스레인지.png",
    "가위": f"{base_path}\\가위.png",
    "감자칼": f"{base_path}\\감자칼.png",
    "도마": f"{base_path}\\도마.png",
    "라면냄비": f"{base_path}\\라면냄비.png",
    "부르스타": f"{base_path}\\부르스타.png",
    "솥냄비": f"{base_path}\\솥냄비.png",
    "없어요": f"{base_path}\\없어요.png",
    "인덕션": f"{base_path}\\인덕션.png",
    "전자레인지": f"{base_path}\\전자레인지.png",
    "칼": f"{base_path}\\칼.png",
    "후라이팬": f"{base_path}\\후라이팬.png",
}
selected_tools = multiselect_by_image("사용할 도구를 골라 주세요", tool_imgs)

# ── 3) 이동 버튼 ────────────────────────────────────────
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
            switch_page("1_재료선택.py")
