import streamlit as st
from pathlib import Path
from streamlit_image_select import image_select
import base64

# ── TTS: 브라우저 Web Speech API 사용 ────────────────────────
def speak(text: str):
    """TTS wrapper (uses the browser's Web Speech API)."""
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

# ── 단일 선택 + 클릭 시 테두리 표시/해제 ─────────────────────────
def select_one_by_image(label: str, options: dict[str, Path], per_row: int = 4):
    st.write(f"#### {label}")

    if "last_selected_path" not in st.session_state:
        st.session_state.last_selected_path = None

    paths = list(options.values())
    captions = list(options.keys())

    remainder = len(paths) % per_row
    if remainder != 0:
        blank_img = str(Path("data/blank.png"))
        for _ in range(per_row - remainder):
            paths.append(Path(blank_img))
            captions.append("")

    selected_path = image_select(
        label="",
        images=[str(p) for p in paths],
        captions=captions,
    )

    # 토글 동작
    if selected_path == st.session_state.last_selected_path:
        st.session_state.last_selected_path = None
        return None
    else:
        st.session_state.last_selected_path = selected_path

    # 선택된 경우 테두리 있는 HTML 렌더링
    if selected_path and Path(selected_path).name != "blank.png":
        idx = paths.index(Path(selected_path))
        name = captions[idx]

        border_style = "5px solid red"
        st.markdown(
            f"""
            <div style="position:relative; display:inline-block; border:{border_style}; border-radius:10px;">
                <img src="data:image/png;base64,{base64.b64encode(open(paths[idx], "rb").read()).decode()}" style="width:100%; border-radius:10px;">
            </div>
            """,
            unsafe_allow_html=True
        )

        speak(f"{name} 선택")
        return name
    return None
