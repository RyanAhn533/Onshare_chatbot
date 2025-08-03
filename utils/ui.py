# utils/ui.py
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

# ── 공통 이미지-버튼 위젯 (라디오/토글) ─────────────────────
def multiselect_by_image_overlay(label: str, options: dict[str, Path], per_row: int = 5):
    """이미지 위에 버튼이 겹쳐서 클릭 가능하게 구성된 이미지 멀티 셀렉트"""
    st.write(f"#### {label}")
    states = {}

    keys = list(options.keys())

    for i in range(0, len(keys), per_row):
        row_keys = keys[i:i + per_row]
        cols = st.columns(per_row)

        for j in range(per_row):
            col = cols[j]
            if j < len(row_keys):
                name = row_keys[j]
                img = options[name]
                key = f"sel_{name}"

                if key not in st.session_state:
                    st.session_state[key] = False

                selected = st.session_state[key]
                border = "5px solid #ff8c00" if selected else "1px solid #ccc"

                # 고유 버튼 키 (버튼 충돌 방지)
                button_key = f"btn_overlay_{name}"

                # 이미지 + 겹쳐진 버튼 UI
                html = f"""
                <div style="position: relative; width: 100%; text-align:center;">
                    <img src="data:image/png;base64,{_b64_png(img)}"
                         style="width:100%;padding:4px;border:{border};border-radius:12px;">
                    <form action="" method="post">
                        <input type="submit" name="{button_key}" value=""
                            style="position:absolute;top:0;left:0;width:100%;height:100%;
                                   opacity:0;cursor:pointer;border:none;">
                    </form>
                    <div style='margin-top: 4px; font-weight: bold; font-size: 1.1rem'>{name}</div>
                </div>
                """

                # HTML 클릭 처리
                submitted = col.form(key=f"form_{name}").form_submit_button(label="", help=name)
                if submitted:
                    st.session_state[key] = not selected
                    speak(f"{name} {'선택' if st.session_state[key] else '해제'}")

                col.markdown(html, unsafe_allow_html=True)
                states[name] = st.session_state[key]
            else:
                col.markdown("&nbsp;")

    return [k for k, v in states.items() if v]




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
