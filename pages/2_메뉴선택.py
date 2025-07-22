## 메뉴 선택
import streamlit as st
from utils.ui import multiselect_by_image, speak
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
speak("오늘 만들 메뉴를 하나 골라 주세요.")

# ── 요리 이미지 목록 불러오기 ──
menu_imgs = {p.stem: p for p in Path("data/menu").glob("*.png")}
menu = multiselect_by_image("메뉴를 선택하세요 (1개)", menu_imgs)

# ── 다음 단계 버튼 ──
if menu and st.button("요리 시작하기 ▶️"):
    st.session_state["menu"] = menu[0]
    st.switch_page("pages/3_만드는방법.py")
