## 재료 고르기
import streamlit as st
from utils.ui import multiselect_by_image, speak
from pathlib import Path

# ── 페이지 설정 ──
st.set_page_config(page_title="② 재료 선택", page_icon="🥕")

# ── 상단 고정 제목 ──
st.markdown("""
    <div style='text-align: center; margin-top: -40px; margin-bottom: 30px;'>
        <h1>🍳 요리용 챗봇 온쿡</h1>
    </div>
""", unsafe_allow_html=True)

# ── 이 페이지 전용 부제목 ──
st.subheader("② 집에 있는 재료를 선택해주세요")

# 음성 안내
speak("집에 있는 재료를 모두 골라 주세요.")

# ── 재료 이미지 불러오기 ──
ing_imgs = {p.stem: p for p in Path("data/ingredients").glob("*.png")}
selected_ings = multiselect_by_image("재료를 선택하세요", ing_imgs)

# ── 다음 단계 버튼 ──
if st.button("다음 단계로 ➡️"):
    st.session_state["selected_ingredients"] = selected_ings or ["없음"]
    st.switch_page("pages/2_메뉴선택.py")
