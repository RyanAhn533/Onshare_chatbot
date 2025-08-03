# utils/ui.py
import streamlit as st
from pathlib import Path
import base64
from pathlib import Path

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

                # 👉 진짜 버튼 대신 HTML 내부 버튼처럼 표현하고, 클릭은 st.button으로 처리
                if col.button("", key=f"btn_{name}"):
                    st.session_state[key] = not is_selected

                # 버튼 아래 이미지 삽입 (버튼을 '위에 빈칸'처럼 보이게)
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
    개선된 AAC 제어 패널 – 이미지 위에 호버 효과, 카드형 버튼, 깔끔한 정렬
    controls = {"시작": (Path(...), "요리를 시작할게요"), ...}
    callback(label)  # 버튼 클릭 시 라벨만 넘김
    """
    st.write("#### 🔘 제어 패널")
    cols = st.columns(len(controls))

    for col, (label, (img, _)) in zip(cols, controls.items()):
        button_key = f"aac_{label}"

        # 선택 시 콜백 호출
        if col.button(label, key=button_key):
            callback(label)

        # 이미지 카드 스타일로 마크다운 표시
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
