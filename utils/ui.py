# utils/ui.py
import streamlit as st
from pathlib import Path
import base64

# ── 내부 util ───────────────────────────────────────────────
def _b64_png(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()

def speak(text: str):
    st.components.v1.html(
        f"""
        <script>
          window.speechSynthesis.cancel();
          window.speechSynthesis.speak(
            new SpeechSynthesisUtterance("{text}")
          );
        </script>
        """,
        height=0,
    )

# ── 공통 이미지-버튼 위젯 (라디오/토글) ─────────────────────
def multiselect_by_image(label: str, options: dict[str, Path]):
    """여러 장 중 ‘여러 개’를 토글 선택"""
    st.write(f"#### {label}")
    cols = st.columns(len(options))
    states = {}

    for col, (name, img) in zip(cols, options.items()):
        key = f"sel_{name}"
        if key not in st.session_state:
            st.session_state[key] = False

        if col.button("", key=f"btn_{name}"):
            st.session_state[key] = not st.session_state[key]
            speak(f"{name} {'선택' if st.session_state[key] else '해제'}")

        border = "5px solid #ff8c00" if st.session_state[key] else "1px solid #ccc"
        col.markdown(
            f"<img src='data:image/png;base64,{_b64_png(img)}' "
            f"style='width:100%;padding:4px;border:{border};border-radius:12px;' title='{name}'>",
            unsafe_allow_html=True,
        )
        col.caption(name)
        states[name] = st.session_state[key]

    return [k for k, v in states.items() if v]


def select_one_by_image(label: str, options: dict[str, Path]):
    """여러 장 중 ‘하나’를 고르는 단일 선택"""
    st.write(f"#### {label}")
    cols = st.columns(len(options))
    choice = st.session_state.get(f"_single_{label}", None)

    for col, (name, img) in zip(cols, options.items()):
        if col.button("", key=f"btn_{label}_{name}"):
            choice = name
            st.session_state[f"_single_{label}"] = name
            speak(f"{name} 선택")

        border = "5px solid #ff8c00" if choice == name else "1px solid #ccc"
        col.markdown(
            f"<img src='data:image/png;base64,{_b64_png(img)}' "
            f"style='width:100%;padding:4px;border:{border};border-radius:12px;' title='{name}'>",
            unsafe_allow_html=True,
        )
        col.caption(name)

    return choice


# ── Assistant 전용 : 제어(AAC) 버튼 묶음 ──────────────────
def aac_control_panel(controls: dict[str, tuple[Path, str]], callback):
    """
    controls = {
        '시작': (Path('data/aac_controls/start.png'), '요리를 시작할게요.'),
        '다음': (Path('data/aac_controls/next.png'),  '다음 단계 알려줘.'),
        …
    }
    callback(msg)  # 클릭 시 호출
    """
    cols = st.columns(len(controls))
    for col, (label, (img, msg)) in zip(cols, controls.items()):
        if col.button("", key=f"aac_{label}"):
            callback(msg)
        col.markdown(
            f"<img src='data:image/png;base64,{_b64_png(img)}' "
            f"style='width:100%;padding:4px;border:1px solid #ccc;border-radius:12px;' title='{label}'>",
            unsafe_allow_html=True,
        )
        col.caption(label)

def aac_control_panel(controls: dict[str, tuple[Path, str]], callback):
    """
    controls = {"시작": (Path(...), "임의 텍스트"), ...}
    callback(label)  # 버튼 라벨만 넘김
    """
    cols = st.columns(len(controls))
    for col, (label, (img, _)) in zip(cols, controls.items()):
        if col.button("", key=f"aac_{label}"):
            callback(label)
        col.markdown(
            f"<img src='data:image/png;base64,{_b64_png(img)}' "
            f"style='width:100%;padding:4px;border:1px solid #ccc;border-radius:12px;' title='{label}'>",
            unsafe_allow_html=True,
        )
        col.caption(label)
