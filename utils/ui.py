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

# ── 이미지 클릭 다중 선택 ─────────────────────────────────
def multiselect_by_image(label: str, options: dict[str, Path], per_row: int = 4):
    st.write(f"#### {label}")
    selected = {}

    keys = list(options.keys())
    for i in range(0, len(keys), per_row):
        row_keys = keys[i:i + per_row]
        cols = st.columns(per_row)

        for j in range(per_row):
            col = cols[j]
            if j < len(row_keys):
                name = row_keys[j]
                img_path = options[name]
                key = f"sel_{name}"

                if key not in st.session_state:
                    st.session_state[key] = False

                is_selected = st.session_state[key]
                border = "4px solid #ff8c00" if is_selected else "2px solid #ccc"
                b64_img = base64.b64encode(img_path.read_bytes()).decode()

                if col.button("", key=f"btn_{name}"):
                    st.session_state[key] = not is_selected

                col.markdown(
                    f"""
                    <div style='text-align:center;'>
                        <img src='data:image/png;base64,{b64_img}'
                             style='width:100%; border-radius:12px; border:{border};'>
                        <div style='margin-top:6px; font-weight:bold; font-size:1.1rem;'>{name}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                selected[name] = st.session_state[key]
            else:
                col.markdown("&nbsp;")

    return [k for k, v in selected.items() if v]

# ── 이미지 클릭 단일 선택 ─────────────────────────────────
def select_one_by_image(label: str, options: dict[str, Path]):
    st.write(f"#### {label}")
    cols = st.columns(len(options))
    choice = st.session_state.get(f"_single_{label}", None)

    for col, (name, img_path) in zip(cols, options.items()):
        key = f"_single_{label}_{name}"

        is_selected = (choice == name)
        border = "5px solid #ff8c00" if is_selected else "1px solid #ccc"
        b64_img = base64.b64encode(img_path.read_bytes()).decode()

        if col.button("", key=key):
            choice = name
            st.session_state[f"_single_{label}"] = name
            speak(f"{name} 선택")

        col.markdown(
            f"""
            <div style='text-align:center;'>
                <img src='data:image/png;base64,{b64_img}'
                     style='width:100%; border-radius:12px; border:{border};'>
                <div style='margin-top:6px; font-weight:bold; font-size:1.1rem;'>{name}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    return choice

# ── Assistant 전용 : 제어(AAC) 버튼 묶음 ──────────────────
def aac_control_panel(controls: dict[str, tuple[Path, str]], callback):
    st.write("#### 🔘 제어 패널")
    cols = st.columns(len(controls))

    for col, (label, (img, _)) in zip(cols, controls.items()):
        button_key = f"aac_{label}"

        if col.button(label, key=button_key):
            callback(label)

        html = f"""
        <div style="text-align:center; margin-top:-0.5rem;">
            <div style="
                border-radius: 16px;
                border: 2px solid #ccc;
                padding: 8px;
                transition: 0.2s;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
            " onmouseover="this.style.border='2px solid #ff8c00';"
              onmouseout="this.style.border='2px solid #ccc';">
                <img src="data:image/png;base64,{_b64_png(img)}"
                     style="width:100%; height:auto; border-radius: 12px;">
                <div style="font-weight:600; font-size:1.05rem; margin-top:6px;">{label}</div>
            </div>
        </div>
        """
        col.markdown(html, unsafe_allow_html=True)