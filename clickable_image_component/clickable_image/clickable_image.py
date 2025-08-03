import os
import streamlit as st
import streamlit.components.v1 as components

_component_func = components.declare_component(
    "clickable_image_selector",
    path=os.path.join(os.path.dirname(__file__), "frontend/build"),
)

def clickable_image_selector(images):
    return _component_func(images=images, default=[])
