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


# ── 다중 선택 (streamlit-image-select는 단일 선택만 지원) ─────────────

def multiselect_by_image(label: str, options: dict[str, Path], per_row: int = 4):
    st.write(f"#### {label}")
    selected = []

    keys = list(options.keys())
    for i in range(0, len(keys), per_row):
        row_keys = keys[i:i + per_row]
        cols = st.columns(per_row)

        for j, key in enumerate(row_keys):
            with cols[j]:
                st.image(str(options[key]), use_container_width=True)
                if st.checkbox(f"{key}", key=f"{label}_{key}"):
                    selected.append(key)

    return selected


# ── 단일 선택: image_select 간단 사용 ──────────────────────────────

def select_one_by_image(label: str, options: dict[str, Path]):
    st.write(f"#### {label}")

    paths = list(options.values())
    captions = list(options.keys())

    selected_path = image_select(
        label="",
        images=[str(p) for p in paths],
        captions=captions,
        image_size=(200, 200),  # 👈 여기서 크기 고정 (원본 비율 유지하려면 height만 지정하거나 auto도 가능)
    )

    if selected_path:
        name = captions[paths.index(Path(selected_path))]
        speak(f"{name} 선택")
        return name
    return None


# ── 제어 패널: 단일 선택처럼 사용 후 콜백 호출 ───────────────────────

def aac_control_panel(controls: dict[str, tuple[Path, str]], callback):
    st.write("#### 🔘 제어 패널")

    labels = list(controls.keys())
    images = [str(p[0]) for p in controls.values()]
    captions = labels

    selected_path = image_select(
        label="",
        images=images,
        captions=captions,
        image_size=(160, 160),  # 👈 필요에 따라 크기 조정
    )

    if selected_path:
        index = images.index(selected_path)
        label = labels[index]
        speak_text = controls[label][1]
        callback(label)
        speak(speak_text)
