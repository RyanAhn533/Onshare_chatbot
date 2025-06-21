# pages/3_Assistant.py
import streamlit as st
from pathlib import Path
from utils.ui import speak, aac_control_panel
from utils.gpt_helper import ask_gpt

st.set_page_config(page_title="④ 요리 도우미", page_icon="👩‍🍳")

# ── 앞 단계 정보 가져오기 ──────────────────────────────────
menu        = st.session_state.get("menu")
ingredients = st.session_state.get("selected_ingredients")
tools       = st.session_state.get("selected_tools")
hand        = st.session_state.get("hand_status")

if not all([menu, ingredients, tools, hand]):
    st.error("이전 단계 정보가 없어요. 처음부터 다시 진행해 주세요.")
    st.stop()

# ── 레시피 한꺼번에 받아 두기 (Start 클릭 시) ────────────────
def fetch_recipe():
    context = (
        f"손 상태: {hand}\n"
        f"도구: {', '.join(tools)}\n"
        f"재료: {', '.join(ingredients)}\n"
        f"메뉴: {menu}\n"
    )
    prompt = (
        context
        + "위 정보를 참고해 쉬운 한국어로 요리 과정을 한 문장씩 나눠 주세요. "
          "각 문장은 ①, ② 처럼 번호만 붙이고, 15단계 이하로 해 주세요. "
          "불필요한 인삿말 없이 과정만 주세요."
    )
    msgs = [
        {"role": "system",
         "content": "당신은 발달장애인을 돕는 초등학교 선생님입니다. "
                    "항상 짧고 쉬운 문장으로 요리 단계를 설명하세요."},
        {"role": "user", "content": prompt},
    ]
    raw = ask_gpt(msgs)
    # 번호·줄바꿈 기준으로 단계 리스트 추출
    steps = [s.lstrip("①②③④⑤⑥⑦⑧⑨⑩⓫⓬⓭⓮⓯ ").strip()
             for s in raw.splitlines() if s.strip()]
    st.session_state["recipe_steps"] = steps
    st.session_state["step_idx"] = 0

# ── 현재 단계 보여 주기 ────────────────────────────────────
def show_current_step():
    idx = st.session_state.get("step_idx", 0)
    steps = st.session_state.get("recipe_steps", [])
    if not steps:
        st.info("‘시작’ 버튼을 눌러 요리를 시작해 주세요.")
        return
    if idx >= len(steps):
        st.success("모든 단계가 끝났어요! 맛있게 드세요 😊")
        speak("모든 단계가 끝났어요! 맛있게 드세요.")
        return
    step_txt = f"### {idx+1}/{len(steps)}단계\n\n{steps[idx]}"
    st.markdown(step_txt)
    if st.session_state.get("_spoken_idx") != idx:  # 같은 단계에서 중복 음성 방지
        speak(steps[idx])
        st.session_state["_spoken_idx"] = idx

# ── 버튼 콜백 ──────────────────────────────────────────────
def on_start(_):
    if "recipe_steps" not in st.session_state:
        fetch_recipe()
    show_current_step()

def on_next(_):
    if "recipe_steps" in st.session_state:
        st.session_state["step_idx"] += 1
    show_current_step()

def on_again(_):
    show_current_step()      # 그대로 다시 읽기

def on_stop(_):
    st.session_state["step_idx"] = 1e9   # 강제로 끝으로
    show_current_step()

# ── AAC 버튼 세트 ─────────────────────────────────────────
controls = {
    "시작": (Path("data/aac_controls/start.png"),  on_start),
    "다음": (Path("data/aac_controls/next.png"),   on_next),
    "다시": (Path("data/aac_controls/again.png"),  on_again),
    "그만": (Path("data/aac_controls/stop.png"),   on_stop),
}
aac_control_panel(
    {k: (v[0], "") for k, v in controls.items()},   # ui.py 시그니처 맞추기용
    lambda lbl: controls[lbl][1](lbl)               # lbl은 버튼 라벨
)

# ── 화면 최초 표지 ────────────────────────────────────────
show_current_step()
