import streamlit as st
from pathlib import Path
from utils.ui import select_one_by_image, speak
from utils.gpt_helper import ask_gpt

st.set_page_config(page_title="③ 메뉴 추천", page_icon="🍽️")
st.markdown("""
    <div style='text-align: center; margin-top: -40px; margin-bottom: 30px;'>
        <h1>🍳 요리용 챗봇 온쿡</h1>
    </div>
""", unsafe_allow_html=True)

st.subheader("③ 만들 수 있는 요리를 골라 주세요")
speak("오늘 만들 메뉴를 하나 골라 주세요.")

ingredients = st.session_state.get("selected_ingredients", [])
tools = st.session_state.get("selected_tools", [])
hand = st.session_state.get("hand_status", "양손")

if not ingredients or not tools:
    st.error("이전 단계에서 선택한 재료와 도구 정보가 없습니다. 처음부터 다시 진행해 주세요.")
    st.stop()

system_prompt = """다음은 요리 이름과 해당 요리를 만들기 위해 꼭 필요한 재료 목록이야:

- 간장계란밥: 계란, 밥, 간장
- 계란후라이: 계란, 기름
- 라면: 라면
- 카레: 카레가루, 감자, 당근, 양파
- 샌드위치: 식빵, 햄, 치즈
- 피자: 피자도우, 치즈, 토마토소스
- 햄버거: 햄버거빵, 패티, 케첩
- 삼계탕: 닭, 찹쌀, 마늘, 파, 부추, 삼계탕육수팩, 소금
- 밀푀유나베: 숙주나물, 알배추, 샤브샤브용 소고기, 깻잎, 팽이버섯, 표고버섯, 물, 코인육수, 국간장, 쯔유

사용자가 가진 재료 목록이 주어질 거야. 그 재료들로 만들 수 있는 요리를 추천해줘.

추천할 때는:
1. 만들 수 있는 요리 한두 개만 간단히 말해줘.
2. 왜 그 요리를 추천했는지 재료 관점에서 짧게 설명해줘.
3. 너무 길게 설명하거나 잡담하지 말고, 핵심만 말해.
"""

user_prompt = f"내가 가진 재료는 {', '.join(ingredients)}야. 어떤 요리를 만들 수 있어?"

with st.spinner("GPT가 가능한 요리를 생각 중이에요..."):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    gpt_response = ask_gpt(messages, model="gpt-4o")

st.markdown("#### 🍳 요리용 챗봇 온쿡 추천 결과")
st.markdown(gpt_response)

# 메뉴 이미지 상대경로 지정
base_path = Path("C:\chat_bot_aac_final\data\menu")
menu_imgs = {
    "간장계란밥": base_path / "간장계란밥.png",
    "계란후라이": base_path / "계란후라이.png",
    "라면": base_path / "라면.png",
    "밀푀유나베": base_path / "밀푀유나베.png",
    "삼계탕": base_path / "삼계탕.png",
    "샌드위치": base_path / "샌드위치.png",
    "카레": base_path / "카레.png",
    "피자": base_path / "피자.png",
    "햄버거": base_path / "햄버거.png",
}

menu = select_one_by_image(
    "메뉴를 선택하세요",
    options=menu_imgs
)

if menu and st.button("요리 시작하기 ▶️"):
    st.session_state["menu"] = menu
    st.session_state["gpt_response"] = gpt_response
    st.switch_page("pages/3_만드는방법.py")
