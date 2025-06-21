# pages/2_Menu.py
import streamlit as st
from utils.ui import multiselect_by_image, speak
from pathlib import Path

st.set_page_config(page_title="③ 메뉴 선택", page_icon="🍽️")
speak("오늘 만들 메뉴를 하나 골라 주세요.")

menu_imgs = {p.stem: p for p in Path("data/menu").glob("*.png")}
menu = multiselect_by_image("메뉴를 선택하세요 (1개)", menu_imgs)

if menu and st.button("요리 시작하기 ▶️"):
    st.session_state["menu"] = menu[0]
    st.switch_page("pages/3_Assistant.py")
