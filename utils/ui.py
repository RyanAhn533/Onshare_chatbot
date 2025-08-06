import streamlit as st
from pathlib import Path
from streamlit_image_select import image_select
import base64
from typing import Dict, Union
from utils.ui import speak


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

def select_one_by_image(
    label: str,
    options: Dict[str, Union[str, Path]],
    img_size: tuple = (200, 200),
    container_width: bool = False
):
    """
    하나의 이미지를 선택하는 UI.
    
    Args:
        label (str): 상단 안내 라벨
        options (dict): {이름: Path or str} 형태의 이미지 목록
        img_size (tuple): (width, height) 픽셀 크기
        container_width (bool): True면 화면 폭에 맞춤
    """
    st.write(f"#### {label}")

    # Path를 문자열로 변환
    paths = [str(p) for p in options.values()]
    captions = list(options.keys())

    selected_path = image_select(
        label="",
        images=paths,
        captions=captions,
        use_container_width=container_width,
        image_size=img_size
    )

    if selected_path:
        # 선택된 파일명 → options key 찾기
        try:
            name = captions[paths.index(selected_path)]
        except ValueError:
            name = Path(selected_path).stem

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
