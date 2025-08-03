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
    
    # 세션 상태 초기화
    if 'multi_image_selection' not in st.session_state:
        st.session_state.multi_image_selection = set()

    selected_keys = st.session_state.multi_image_selection

    keys = list(options.keys())
    for i in range(0, len(keys), per_row):
        row_keys = keys[i:i + per_row]
        cols = st.columns(per_row)

        for j, key in enumerate(row_keys):
            with cols[j]:
                image_path = options[key]
                button_key = f"{label}_{key}_btn"

                # 이미지 위에 버튼을 투명하게 덮어서 이미지 클릭 시 선택되도록 처리
                clicked = st.button(
                    label=" ",  # 버튼 텍스트 없음
                    key=button_key,
                    help=key
                )
                st.image(str(image_path), caption=key, use_container_width=True)

                # 클릭되었을 때 상태 토글
                if clicked:
                    if key in selected_keys:
                        selected_keys.remove(key)
                    else:
                        selected_keys.add(key)

                # 선택된 경우 강조
                if key in selected_keys:
                    st.markdown(f"<div style='text-align:center; color:green;'>✅ 선택됨</div>", unsafe_allow_html=True)

    return list(selected_keys)


# ── 단일 선택: image_select 기본 사용 ──────────────────────────────

def select_one_by_image(label: str, options: dict[str, Path]):
    st.write(f"#### {label}")

    paths = list(options.values())
    captions = list(options.keys())

    selected_path = image_select(
        label="",
        images=[str(p) for p in paths],
        captions=captions,
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
    )

    if selected_path:
        index = images.index(selected_path)
        label = labels[index]
        speak_text = controls[label][1]
        callback(label)
        speak(speak_text)
