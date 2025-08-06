import streamlit as st
from pathlib import Path
from streamlit_image_select import image_select
import streamlit as st

def switch_page(page_name: str):
    from streamlit_extras.switch_page_button import switch_page as sp
    sp(page_name)

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

# ── 단일 선택: 선택된 건 테두리 표시 ──────────────────────────────
def select_one_by_image(label: str, options: dict[str, Path], per_row: int = 4):
    st.write(f"#### {label}")

    if "last_selected_path" not in st.session_state:
        st.session_state.last_selected_path = None
    if "selected_menu" not in st.session_state:
        st.session_state.selected_menu = None

    paths = list(options.values())
    captions = list(options.keys())

    # 빈 칸 채우기
    remainder = len(paths) % per_row
    if remainder != 0:
        blank_img = str(Path("data/blank.png"))
        for _ in range(per_row - remainder):
            paths.append(Path(blank_img))
            captions.append("")

    # 이미지 선택
    selected_path = image_select(
        label="",
        images=[str(p) for p in paths],
        captions=captions,
    )

    # blank는 무시
    if not selected_path or Path(selected_path).name == "blank.png":
        return st.session_state.selected_menu

    # 토글 처리
    if selected_path == st.session_state.last_selected_path:
        # 선택 해제
        st.session_state.last_selected_path = None
        st.session_state.selected_menu = None
        return None
    else:
        # 새 선택
        st.session_state.last_selected_path = selected_path
        idx = paths.index(Path(selected_path))
        name = captions[idx]
        st.session_state.selected_menu = name
        speak(f"{name} 선택")
        return name



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
