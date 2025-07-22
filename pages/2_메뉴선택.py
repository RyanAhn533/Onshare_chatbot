## 요리 메뉴 선택
import streamlit as st
from utils.ui import select_one_by_image, speak
from pathlib import Path

# ── 페이지 설정 ──
st.set_page_config(page_title="③ 메뉴 선택", page_icon="🍽️")

# ── 상단 고정 제목 ──
st.markdown("""
    <div style='text-align: center; margin-top: -40px; margin-bottom: 30px;'>
        <h1>🍳 요리용 챗봇 온쿡</h1>
    </div>
""", unsafe_allow_html=True)

# ── 이 페이지 전용 부제목 ──
st.subheader("③ 먹고 싶은 요리를 골라주세요!")

# 음성 안내
speak("먹고 싶은 요리를 한 가지 골라 주세요.")

# ── 요리 이미지 목록 불러오기 ──
menu_imgs = {p.stem: p for p in Path("data/menus").glob("*.png")}
menu = select_one_by_image("어떤 요리를 만들고 싶나요?", menu_imgs)

# ── 다음 단계 버튼 ──
if st.button("요리 시작하기 ▶️"):
    if menu is None:
        st.warning("원하는 요리를 먼저 골라 주세요.")
        speak("요리를 먼저 골라 주세요.")
    else:
        st.session_state["menu"] = menu
        st.switch_page("pages/3_만드는방법.py")  # 다음 단계 파일명에 맞게 수정
