import streamlit as st
from pathlib import Path
import base64

# ── 내부 util ───────────────────────────────────────────────

def _b64_png(path: Path) -> str:
    """Convert a local PNG file to base-64 string."""
    return base64.b64encode(path.read_bytes()).decode()


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


# ── 이미지 위 클릭 영역이 버튼 역할을 하도록 수정된 다중 선택 ─────────────

def multiselect_by_image(label: str, options: dict[str, Path], per_row: int = 4):
    st.write(f"#### {label}")
    selected = {}

    keys = list(options.keys())
    for i in range(0, len(keys), per_row):
        row_keys = keys[i: i + per_row]
        cols = st.columns(per_row)

        for j, col in enumerate(cols):
            if j >= len(row_keys):
                col.markdown("&nbsp;")
                continue

            name = row_keys[j]
            img_path = options[name]
            btn_key = f"btn_multi_{name}"
            state_key = f"sel_multi_{name}"

            if state_key not in st.session_state:
                st.session_state[state_key] = False

            is_selected = st.session_state[state_key]
            checkbox_bg = "#ff8c00" if is_selected else "rgba(255,255,255,0.75)"
            checkmark = "✓" if is_selected else "&nbsp;"

            b64_img = _b64_png(img_path)

            clicked = col.button(" ", key=btn_key)
            if clicked:
                st.session_state[state_key] = not is_selected

            col.markdown(
                f"""
                <style>
                    [data-testid="baseButton-{btn_key}"] {{
                        position: absolute;
                        top: 0; left: 0; right: 0; bottom: 0;
                        opacity: 0;
                        z-index: 10;
                        width: 100%;
                        height: 100%;
                    }}
                </style>
                <div style='position:relative; text-align:center; margin-bottom:10px;'>
                    <label for="{btn_key}" style="display:block; position:relative; cursor:pointer;">
                        <img src='data:image/png;base64,{b64_img}'
                             style='width:100%; border-radius:12px; border:2px solid {checkbox_bg};'>
                        <div style="position:absolute; top:8px; right:8px;
                                    width:26px; height:26px;
                                    border-radius:4px; border:2px solid #666;
                                    background:{checkbox_bg};
                                    display:flex; align-items:center; justify-content:center;
                                    font-weight:900; color:white;">
                            {checkmark}
                        </div>
                    </label>
                    <div style='margin-top:6px; font-weight:bold; font-size:1.05rem;'>{name}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            selected[name] = st.session_state[state_key]

    return [k for k, v in selected.items() if v]


# ── 이미지 위 클릭 영역이 버튼 역할을 하도록 수정된 단일 선택 ─────────────

def select_one_by_image(label: str, options: dict[str, Path]):
    st.write(f"#### {label}")

    choice_key = f"single_choice_{label}"
    current_choice = st.session_state.get(choice_key)

    cols = st.columns(len(options))
    for col, (name, img_path) in zip(cols, options.items()):
        btn_key = f"btn_single_{label}_{name}"

        is_selected = current_choice == name
        checkbox_bg = "#ff8c00" if is_selected else "rgba(255,255,255,0.75)"
        checkmark = "✓" if is_selected else "&nbsp;"

        b64_img = _b64_png(img_path)

        clicked = col.button(" ", key=btn_key)
        if clicked:
            st.session_state[choice_key] = name
            speak(f"{name} 선택")
            current_choice = name

        col.markdown(
            f"""
            <style>
                [data-testid="baseButton-{btn_key}"] {{
                    position: absolute;
                    top: 0; left: 0; right: 0; bottom: 0;
                    opacity: 0;
                    z-index: 10;
                    width: 100%;
                    height: 100%;
                }}
            </style>
            <div style='position:relative; text-align:center; margin-bottom:10px;'>
                <label for="{btn_key}" style="display:block; position:relative; cursor:pointer;">
                    <img src='data:image/png;base64,{b64_img}'
                         style='width:100%; border-radius:12px; border:2px solid {checkbox_bg};'>
                    <div style="position:absolute; top:8px; right:8px;
                                width:26px; height:26px;
                                border-radius:4px; border:2px solid #666;
                                background:{checkbox_bg};
                                display:flex; align-items:center; justify-content:center;
                                font-weight:900; color:white;">
                        {checkmark}
                    </div>
                </label>
                <div style='margin-top:6px; font-weight:bold; font-size:1.05rem;'>{name}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    return st.session_state.get(choice_key)


# ── 제어 패널도 동일하게 이미지 클릭 = 버튼 동작으로 적용 가능 ───────

def aac_control_panel(controls: dict[str, tuple[Path, str]], callback):
    st.write("#### 🔘 제어 패널")
    cols = st.columns(len(controls))

    for col, (label, (img, speak_text)) in zip(cols, controls.items()):
        button_key = f"aac_{label}"
        state_key = f"aac_state_{label}"
        if state_key not in st.session_state:
            st.session_state[state_key] = False

        is_active = st.session_state[state_key]
        checkbox_bg = "#ff8c00" if is_active else "rgba(255,255,255,0.75)"
        checkmark = "✓" if is_active else "&nbsp;"

        clicked = col.button(" ", key=button_key)
        if clicked:
            st.session_state[state_key] = not is_active
            callback(label)
            speak(speak_text)

        b64_img = _b64_png(img)
        col.markdown(
            f"""
            <style>
                [data-testid="baseButton-{button_key}"] {{
                    position: absolute;
                    top: 0; left: 0; right: 0; bottom: 0;
                    opacity: 0;
                    z-index: 10;
                    width: 100%;
                    height: 100%;
                }}
            </style>
            <div style="text-align:center; position:relative; margin-top:-0.3rem;">
                <label for="{button_key}" style="display:block; position:relative; cursor:pointer;">
                    <img src="data:image/png;base64,{b64_img}"
                         style="width:100%; height:auto; border-radius: 12px; border:2px solid {checkbox_bg};" />
                    <div style="position:absolute; top:8px; right:8px;
                                width:26px; height:26px;
                                border-radius:4px; border:2px solid #666;
                                background:{checkbox_bg};
                                display:flex; align-items:center; justify-content:center;
                                font-weight:900; color:white;">
                        {checkmark}
                    </div>
                </label>
                <div style="font-weight:600; font-size:1.05rem; margin-top:6px;">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
