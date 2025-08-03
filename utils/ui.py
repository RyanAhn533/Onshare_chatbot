import streamlit as st
from pathlib import Path
from streamlit_image_select import image_select
import base64

# ── 내부 util ───────────────────────────────────────────────

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


# ── 다중 선택: image_select는 기본적으로 단일 선택이므로 커스텀으로 구성 ─────

def multiselect_by_image(label: str, options: dict[str, Path], per_row: int = 4):
    st.write(f"#### {label}")
    selected = []

    cols = st.columns(per_row)
    keys = list(options.keys())

    for i in range(0, len(keys), per_row):
        row_keys = keys[i:i + per_row]
        for j, key in enumerate(row_keys):
            with cols[j]:
                is_selected = st.checkbox(
                    label=key,
                    key=f"multi_{label}_{key}",
                )
                img = options[key]
                st.image(str(img), use_column_width=True)
                if is_selected:
                    selected.append(key)
    return selected


# ── 단일 선택: image_select로 매우 간단하게 구현 가능 ─────────────

def select_one_by_image(label: str, options: dict[str, Path]):
    st.write(f"#### {label}")
    selected = image_select(
        label="",
        images=[str(p) for p in options.values()],
        captions=list(options.keys()),
        use_container_width=True
    )
    if selected:
        name = list(options.keys())[list(options.values()).index(Path(selected))]
        speak(f"{name} 선택")
        return name
    return None


# ── 제어 패널: 단일 선택처럼 보이게 설정, 클릭 시 콜백 호출 ───────────

def aac_control_panel(controls: dict[str, tuple[Path, str]], callback):
    st.write("#### 🔘 제어 패널")

    labels = list(controls.keys())
    images = [str(img_path) for img_path, _ in controls.values()]
    captions = labels

    selected = image_select(
        label="",
        images=images,
        captions=captions,
        use_container_width=True
    )

    if selected:
        label = captions[images.index(selected)]
        speak_text = controls[label][1]
        callback(label)
        speak(speak_text)
