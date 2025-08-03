import streamlit as st
from pathlib import Path
from clickable_image_component.clickable_image.clickable_image import clickable_image_selector

# ── 페이지 전환 래퍼 ─────────────────────────────────────────
def switch_page(page: str):
    if not page.endswith(".py"):
        page += ".py"
    if not page.startswith("pages/"):
        page = f"pages/{page}"
    st.switch_page(page)

# ── TTS 유틸 ────────────────────────────────────────────────
def speak(text: str):
    st.components.v1.html(
        f"""
        <script>
          window.speechSynthesis.cancel();
          window.speechSynthesis.speak(
            new SpeechSynthesisUtterance("{text}")
          );
        </script>
        """,
        height=0,
    )

# ── 페이지 설정 ────────────────────────────────────────────
st.set_page_config(page_title="① 손 씻기 & 도구", page_icon="🍳")

# ── 헤더 ───────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align: center; margin-top: -40px;'>🍳 요리용 챗봇 온쿡</h1>",
    unsafe_allow_html=True,
)
speak("손을 씻었는지 먼저 알려 주시고, 사용할 도구 그림을 눌러 주세요.")

# ── 1) 손 씻음 여부(단일) ──────────────────────────────────
hand_imgs = {
    "손 깨끗해요": "data/hand/clean.png",
    "손 더러워요": "data/hand/dirty.png",
}
hand_choice = clickable_image_selector(hand_imgs)     # 리스트로 리턴
hand_status = hand_choice[0] if hand_choice else None

# ── 2) 준비된 도구(다중) ───────────────────────────────────
tool_imgs = {p.stem: str(p) for p in Path("data/tools").glob("*.png")}
selected_tools = clickable_image_selector(tool_imgs)  # 리스트 그대로

# ── 3) 네비게이션 버튼 ────────────────────────────────────
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
            switch_page("1_재료선택")   # 다음 페이지로 이동
