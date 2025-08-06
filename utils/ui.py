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

    # 세션 초기화
    if "image_select_multi" not in st.session_state:
        st.session_state.image_select_multi = set()

    selected = st.session_state.image_select_multi
    keys = list(options.keys())

    for i in range(0, len(keys), per_row):
        row_keys = keys[i:i + per_row]
        cols = st.columns(per_row)

        for j, key in enumerate(row_keys):
            with cols[j]:
                # 하나의 이미지 선택 UI처럼 구성
                is_selected = key in selected
                # 버튼처럼 동작: 클릭하면 상태 토글
                if st.button(f"✅ {key}" if is_selected else key, key=f"btn_{key}"):
                    if is_selected:
                        selected.remove(key)
                    else:
                        selected.add(key)
                # 이미지 출력
                st.image(str(options[key]), use_container_width=True)

    return list(selected)


# ── 단일 선택: image_select 기본 사용 ──────────────────────────────

def select_one_by_image(label: str, options: dict[str, Path], per_row: int = 4):
    st.write(f"#### {label}")

    # 세션 초기화
    if "image_select_single" not in st.session_state:
        st.session_state.image_select_single = None

    selected_name = st.session_state.image_select_single
    paths = list(options.values())
    captions = list(options.keys())

    remainder = len(paths) % per_row
    if remainder != 0:
        blank_img = str(Path("data/blank.png"))
        for _ in range(per_row - remainder):
            paths.append(Path(blank_img))
            captions.append("")

    # 버튼+이미지로 직접 구현 (image_select 대신)
    for i in range(0, len(paths), per_row):
        cols = st.columns(per_row)
        for j, p in enumerate(paths[i:i+per_row]):
            name = captions[i + j]
            if not name:  # 빈 칸
                cols[j].empty()
                continue

            is_selected = (name == selected_name)
            border_color = "5px solid red" if is_selected else "2px solid transparent"

            with cols[j]:
                if st.button(f"{'✅ ' if is_selected else ''}{name}", key=f"btn_{name}"):
                    if is_selected:
                        st.session_state.image_select_single = None  # 선택 해제
                    else:
                        st.session_state.image_select_single = name
                        speak(f"{name} 선택")

                st.markdown(
                    f"""
                    <div style="border:{border_color}; border-radius:10px; padding:5px;">
                        <img src="data:image/png;base64,{base64.b64encode(open(p, 'rb').read()).decode()}" style="width:100%; border-radius:8px;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    return st.session_state.image_select_single


def select_one_by_image_noempty(label: str, options: dict[str, Path]):
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
