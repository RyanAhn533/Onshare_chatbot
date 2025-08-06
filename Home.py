import streamlit as st
from utils.ui import select_one_by_image, select_one_by_image_noempty, speak
from pathlib import Path

# ── 페이지 이동 함수 ───────────────────────────────
def switch_page(page: str):
    if not page.endswith(".py"):
        page += ".py"
    if not page.startswith("pages/"):
        page = f"pages/{page}"
    st.switch_page(page)

# ── 페이지 설정 ─────────────────────────────────────
st.set_page_config(page_title="① 손 씻기 & 도구", page_icon="🍳")

# ── 제목 & 안내 ─────────────────────────────────────
st.markdown("<h1 style='text-align: center; margin-top: -40px;'>🍳 요리용 챗봇 온쿡</h1>", unsafe_allow_html=True)
speak("손을 씻었는지 먼저 알려 주시고, 사용할 도구 그림을 눌러 주세요.")

# ── 손 씻기 여부 ────────────────────────────────────
hand_imgs = {
    "손 깨끗해요": Path("data/hand/clean.png"),
    "손 더러워요": Path("data/hand/dirty.png"),
}
hand_status = select_one_by_image_noempty("손을 씻었나요?", hand_imgs)

# ── 도구 이미지 사전 ───────────────────────────────
base_path = Path("data/tools")
tool_imgs = {
    "가스레인지": base_path / "가스레인지.png",
    "가위": base_path / "가위.png",
    "감자칼": base_path / "감자칼.png",
    "도마": base_path / "도마.png",
    "라면냄비": base_path / "라면냄비.png",
    "부르스타": base_path / "부르스타.png",
    "솥냄비": base_path / "솥냄비.png",
    "없어요": base_path / "없어요.png",
    "인덕션": base_path / "인덕션.png",
    "전자레인지": base_path / "전자레인지.png",
    "칼": base_path / "칼.png",
    "후라이팬": base_path / "후라이팬.png",
}

# ── 세션 상태 초기화 ───────────────────────────────
if "selected_tools" not in st.session_state:
    st.session_state.selected_tools = []

# ── 도구 선택 (토글) ───────────────────────────────
selected_tool = select_one_by_image("사용할 도구를 골라 주세요", tool_imgs)

if selected_tool:
    if selected_tool in st.session_state.selected_tools:
        st.session_state.selected_tools.remove(selected_tool)
    else:
        st.session_state.selected_tools.append(selected_tool)

# ── 사이드바에 선택된 도구 표시 ─────────────────────
with st.sidebar:
    st.markdown(
        "<h2 style='font-size:1.6em; font-weight:bold;'>🛠 현재까지 선택된 도구</h2>",
        unsafe_allow_html=True
    )

    if st.session_state.selected_tools:
        st.markdown(
            """
            <div style='background-color:#e3f2fd; padding:12px; border-radius:10px;
                        border:2px solid #1976d2; box-shadow: 2px 2px 6px rgba(0,0,0,0.2);'>
            """,
            unsafe_allow_html=True
        )
        for tool in st.session_state.selected_tools:
            st.markdown(
                f"""
                <div style='background-color:#bbdefb; height:32px; 
                            border-radius:15px; font-weight:bold; color:#0d47a1;
                            width:80%; margin:6px auto;
                            display:flex; justify-content:center; align-items:center;'>
                    {tool}
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("아직 선택된 도구가 없습니다.")

# ── 네비게이션 버튼 ───────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬅️ 이전 단계"):
        switch_page("0_시작화면.py")

with col2:
    if st.button("도구 초기화"):
        st.session_state.selected_tools = []

with col3:
    if st.button("다음 단계 ➡️"):
        if not st.session_state.selected_tools:
            st.warning("도구를 최소 한 개 이상 선택해주세요.")
        else:
            switch_page("pages/1_재료선택.py")
