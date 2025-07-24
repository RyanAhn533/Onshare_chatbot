import streamlit as st
from pathlib import Path
from utils.ui import select_one_by_image, speak
from utils.gpt_helper import ask_gpt

# ── 페이지 기본 설정 ──
st.set_page_config(page_title="③ 메뉴 선택", page_icon="🍽️")

st.markdown("""
    <div style='text-align: center; margin-top: -40px; margin-bottom: 30px;'>
        <h1>🍳 요리용 챗봇 온쿡</h1>
    </div>
""", unsafe_allow_html=True)

st.subheader("③ 만들 수 있는 메뉴를 추천할게요")
speak("선택한 재료로 만들 수 있는 메뉴를 추천할게요.")

# ── 사용자 선택 재료 가져오기 ──
user_ingredients = set(st.session_state.get("selected_ingredients", []))

# ── 1단계: 메뉴 데이터베이스 그대로 유지 ──
menu_db = {
    "간장계란밥": {"필수재료": ["계란", "밥", "간장"], "추천재료": ["참기름", "김가루"]},
    "계란후라이": {"필수재료": ["계란", "기름"], "추천재료": ["소금", "버터"]},
    "라면": {"필수재료": ["라면"], "추천재료": ["계란", "파", "김치"]},
    "삼계탕": {"필수재료": ["닭", "찹쌀", "마늘"], "추천재료": ["대추", "인삼", "파", "소금"]},
    "샌드위치": {"필수재료": ["식빵", "햄", "치즈"], "추천재료": ["계란", "양상추", "마요네즈", "토마토"]},
    "카레": {"필수재료": ["카레가루", "감자", "당근", "양파"], "추천재료": ["고기", "브로콜리", "우유"]},
    "피자": {"필수재료": ["피자도우", "치즈", "토마토소스"], "추천재료": ["페퍼로니", "양파", "파프리카", "올리브"]},
    "햄버거": {"필수재료": ["햄버거빵", "패티"], "추천재료": ["양상추", "치즈", "토마토", "양파", "케찹"]}
}

# ── 2단계: GPT 프롬프트 구성 ──
gpt_prompt = f"""
너는 발달장애인을 위한 요리 추천 도우미야.

다음은 메뉴별 필수 재료와 추천 재료야:
{menu_db}

사용자가 가지고 있는 재료는 다음과 같아:
{user_ingredients}

이 재료들로 만들 수 있는 메뉴를 추론해줘.
꼭 모든 필수재료가 없어도 괜찮아. 중요한 재료가 포함되어 있으면 충분히 추천해도 돼.
예를 들어, 닭과 마늘만 있어도 삼계탕을 추천해도 돼.

가장 만들기 쉬운 메뉴 하나만 추천해줘.
형식: 추천 메뉴: 메뉴이름
"""

# ── 3단계: GPT에게 요청 ──
response = ask_gpt([
    {"role": "system", "content": "너는 발달장애인을 위한 요리 추천 선생님이야. 항상 친절하게 단순하게 알려줘."},
    {"role": "user", "content": gpt_prompt}
])

# ── 결과 파싱 ──
menu_name = response.strip().replace("추천 메뉴:", "").strip()
st.session_state["menu"] = menu_name

# ── 메뉴 이미지 선택 UI ──
menu_imgs = {p.stem: p for p in Path("data/menu").glob("*.png")}

if menu_name in menu_imgs:
    st.image(menu_imgs[menu_name], caption=f"GPT 추천 메뉴: {menu_name}")
else:
    st.warning(f"'{menu_name}' 메뉴 이미지가 없어요. 목록 중 하나를 골라주세요.")

# 사용자 수동 선택도 허용
selected = select_one_by_image("마음에 드는 메뉴를 하나 선택하세요", menu_imgs)

if selected and st.button("요리 시작 ▶️"):
    st.session_state["menu"] = selected
    st.switch_page("pages/3_만드는방법.py")
