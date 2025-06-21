# pages/1_Ingredients.py
import streamlit as st
from utils.ui import multiselect_by_image, speak
from pathlib import Path

st.set_page_config(page_title="② 재료 선택", page_icon="🥕")
speak("집에 있는 재료를 모두 골라 주세요.")

ing_imgs = {p.stem: p for p in Path("data/ingredients").glob("*.png")}
selected_ings = multiselect_by_image("재료를 선택하세요", ing_imgs)

if st.button("다음 단계로 ➡️"):
    # 👉 선택 결과를 세션에 저장
    st.session_state["selected_ingredients"] = selected_ings or ["없음"]
    st.switch_page("pages/2_Menu.py")
