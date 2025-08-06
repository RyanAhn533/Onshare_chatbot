import streamlit as st
from utils.ui import select_one_by_image, speak
from pathlib import Path

st.set_page_config(page_title="② 재료 선택", page_icon="🥕")

st.markdown("""
    <div style='text-align: center; margin-top: -40px; margin-bottom: 30px;'>
        <h1>🍳 요리용 챗봇 온쿡</h1>
    </div>
""", unsafe_allow_html=True)

st.subheader("② 집에 있는 재료를 선택해주세요")
speak("집에 있는 재료 중 하나를 선택해 주세요.")

# 재료 이미지
base_path = Path("data/ingredients")
ing_imgs = {
    "가지": base_path / "가지.png",
    "간장": base_path / "간장.png",
    "감자": base_path / "감자.png",
    "검정올리브": base_path / "검정올리브.png",
    "계란": base_path / "계란.png",
    "고구마": base_path / "고구마.png",
    "고추": base_path / "고추.png",
    "국간장": base_path / "국간장.png",
    "꽃상추": base_path / "꽃상추.png",
    "닭고기": base_path / "닭고기.png",
    "당근": base_path / "당근.png",
    "돼지고기": base_path / "돼지고기.png",
    "라면": base_path / "라면.png",
    "레몬": base_path / "레몬.png",
    "마늘": base_path / "마늘.png",
    "바나나": base_path / "바나나.png",
    "배추": base_path / "배추.png",
    "복숭아": base_path / "복숭아.png",
    "브로콜리": base_path / "브로콜리.png",
    "블루베리": base_path / "블루베리.png",
    "빵": base_path / "빵.png",
    "셀러리": base_path / "셀러리.png",
    "소고기": base_path / "소고기.png",
    "소금": base_path / "소금.png",
    "송이버섯": base_path / "송이버섯.png",
    "식빵": base_path / "식빵.png",
    "쌀": base_path / "쌀.png",
    "애호박": base_path / "애호박.png",
    "쯔유": base_path / "쯔유.png",
    "참기름": base_path / "참기름.png",
    "청경채": base_path / "청경채.png",
    "초록올리브": base_path / "초록올리브.png",
    "코인육수": base_path / "코인육수.png",
    "토마토": base_path / "토마토.png",
    "파": base_path / "파.png",
    "파인애플": base_path / "파인애플.png",
    "포도": base_path / "포도.png",
    "표고버섯": base_path / "표고버섯.png",
    "피클": base_path / "피클.png",
    "피자치즈": base_path / "피자치즈.png",
    "황제버섯": base_path / "황제버섯.png",
    "샤브샤브용소고기": base_path / "샤브샤브용소고기.png",
    "생모짜렐라": base_path / "생모짜렐라.png",
    "후추": base_path / "후추.png",
}

# 세션 상태 초기화
if "selected_ingredients" not in st.session_state:
    st.session_state.selected_ingredients = []

# 재료 하나 선택
selected_ing = select_one_by_image(
    label="재료를 선택하세요",
    options=ing_imgs
)

# 선택한 재료 누적 저장
# 선택한 재료 누적 저장
if selected_ing and selected_ing not in st.session_state.selected_ingredients:
    st.session_state.selected_ingredients.append(selected_ing)

# 현재까지 선택된 재료 표시 (태그 스타일)
if st.session_state.selected_ingredients:
    tags_html = " ".join(
        [
            f"<span style='background-color:#f0f0f0; color:#333; padding:6px 12px; "
            f"border-radius:15px; margin:4px; display:inline-block;'>{item}</span>"
            for item in st.session_state.selected_ingredients
        ]
    )
    st.markdown(f"**현재까지 선택된 재료:**<br>{tags_html}", unsafe_allow_html=True)
else:
    st.info("아직 선택된 재료가 없습니다.")

## 버튼
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬅️ 이전 단계"):
        st.switch_page("pages/0_시작화면.py")  # 이전 단계 페이지 경로로 수정

with col2:
    if st.button("재료 초기화"):
        st.session_state.selected_ingredients = []

with col3:
    if st.button("다음 단계 ➡️"):
        if not st.session_state.selected_ingredients:
            st.warning("재료를 최소 한 개 이상 선택해주세요.")
        else:
            st.switch_page("pages/2_메뉴선택.py")
