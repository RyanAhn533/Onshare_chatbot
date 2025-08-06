import streamlit as st
from utils.ui import select_one_by_image, speak
from pathlib import Path

def switch_page(page: str):
    if not page.endswith(".py"):
        page += ".py"
    if not page.startswith("pages/"):
        page = f"pages/{page}"
    st.switch_page(page)

st.set_page_config(page_title="② 재료 선택", page_icon="🥕")

st.markdown("<h1 style='text-align: center; margin-top: -40px;'>🥕 재료 선택</h1>", unsafe_allow_html=True)
speak("재료를 하나씩 선택해 주세요.")

# 세션 상태 초기화
if "selected_ingredients" not in st.session_state:
    st.session_state.selected_ingredients = []

# 재료 이미지
base_path = Path("data/ingredients")
ingredient_imgs = {
    "당근": base_path / "당근.png",
    "감자": base_path / "감자.png",
    "양파": base_path / "양파.png",
    "버섯": base_path / "버섯.png",
    "고기": base_path / "고기.png",
    "없음": base_path / "없음.png",
}

# 한 개씩 선택
ingredient = select_one_by_image("재료를 골라 주세요", ingredient_imgs)

# 누적 저장
if ingredient and ingredient not in st.session_state.selected_ingredients:
    st.session_state.selected_ingredients.append(ingredient)

# 현재까지 선택 표시
st.write("현재까지 선택된 재료:", st.session_state.selected_ingredients)

# 버튼 영역
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ 뒤로"):
        switch_page("home.py")
with col2:
    if st.button("재료 초기화"):
        st.session_state.selected_ingredients = []
with col3:
    if st.button("➡️ 다음 단계"):
        if not st.session_state.selected_ingredients:
            st.warning("재료를 최소 한 개 이상 선택해 주세요.")
        else:
            switch_page("2_메뉴선택.py")
