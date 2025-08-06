import streamlit as st
from utils.ui import select_one_by_image, speak

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
speak("집에 있는 재료 중 하나를 선택해 주세요.")

# ── 재료 이미지 path 하나씩 지정 ──
base_path = r"C:\chat_bot_aac_final\data\ingredients"

ing_imgs = {
    "가지":        f"{base_path}\\가지.png",
    "간장":        f"{base_path}\\간장.png",
    "감자":        f"{base_path}\\감자.png",
    "검정올리브":  f"{base_path}\\검정올리브.png",
    "계란":        f"{base_path}\\계란.png",
    "고구마":      f"{base_path}\\고구마.png",
    "고추":        f"{base_path}\\고추.png",
    "국간장":      f"{base_path}\\국간장.png",
    "꽃상추":      f"{base_path}\\꽃상추.png",
    "닭고기":      f"{base_path}\\닭고기.png",
    "당근":        f"{base_path}\\당근.png",
    "돼지고기":    f"{base_path}\\돼지고기.png",
    "라면":        f"{base_path}\\라면.png",
    "레몬":        f"{base_path}\\레몬.png",
    "마늘":        f"{base_path}\\마늘.png",
    "바나나":      f"{base_path}\\바나나.png",
    "배추":        f"{base_path}\\배추.png",
    "복숭아":      f"{base_path}\\복숭아.png",
    "브로콜리":    f"{base_path}\\브로콜리.png",
    "블루베리":    f"{base_path}\\블루베리.png",
    "빵":          f"{base_path}\\빵.png",
    "셀러리":      f"{base_path}\\셀러리.png",
    "소고기":      f"{base_path}\\소고기.png",
    "소금":        f"{base_path}\\소금.png",
    "송이버섯":    f"{base_path}\\송이버섯.png",
    "식빵":        f"{base_path}\\식빵.png",
    "쌀":          f"{base_path}\\쌀.png",
    "애호박":      f"{base_path}\\애호박.png",
    "쯔유":        f"{base_path}\\쯔유.png",
    "참기름":      f"{base_path}\\참기름.png",
    "청경채":      f"{base_path}\\청경채.png",
    "초록올리브":  f"{base_path}\\초록올리브.png",
    "코인육수":    f"{base_path}\\코인육수.png",
    "토마토":      f"{base_path}\\토마토.png",
    "파":          f"{base_path}\\파.png",
    "파인애플":    f"{base_path}\\파인애플.png",
    "포도":        f"{base_path}\\포도.png",
    "표고버섯":    f"{base_path}\\표고버섯.png",
    "피클":        f"{base_path}\\피클.png",
    "후추":        f"{base_path}\\후추.png",
}

# ── 이미지 선택 UI (크기 확대) ──
selected_ing = select_one_by_image(
    label="재료를 선택하세요",
    options=ing_imgs,
    img_size=(200, 200)  # 기존보다 크게
)

# ── 다음 단계 버튼 ──
if st.button("다음 단계로 ➡️"):
    st.session_state["selected_ingredients"] = [selected_ing] if selected_ing else ["없음"]
    st.switch_page("pages/2_메뉴선택.py")
