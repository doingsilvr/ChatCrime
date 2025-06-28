import streamlit as st
import openai
from datetime import datetime

# ==================== 초기 설정 ====================
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="AI 탐정", layout="wide")
st.title("🕵️ AI 탐정: 숨겨진 진실을 밝혀라")

# ==================== 세션 상태 초기화 ====================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "clues" not in st.session_state:
    st.session_state.clues = []
if "hint_count" not in st.session_state:
    st.session_state.hint_count = 0

# ==================== 등장인물 설정 ====================
CHARACTER_PROMPT = {
    "Ellen (큐레이터)": "당신은 피해자의 동료 큐레이터 엘렌입니다. 이성적이고 방어적이며 피해자와 최근 갈등이 있었습니다.",
    "Mark (사진작가)": "당신은 감정 기복이 심한 사진작가 마크입니다. 피해자와 돈 문제로 갈등이 있었고, 공격적인 반응을 보이기도 합니다.",
    "Julia (청소 직원)": "당신은 조용한 청소 직원 줄리아입니다. 피해자를 가장 먼저 발견했으며, 말수가 적고 소극적으로 응답합니다."
}

# ==================== GPT 응답 함수 ====================
def get_character_response(character, user_input):
    prompt = f"""
당신은 {character}입니다.
{CHARACTER_PROMPT[character]}

탐정의 질문: "{user_input}"
{character}:"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# ==================== 힌트 제공 함수 ====================
def get_hint():
    hints = [
        "CCTV에는 Mark가 사건 당일 늦게까지 갤러리에 머문 장면이 포착되었습니다.",
        "Ellen과 피해자 사이에는 작품 소유권을 둘러싼 이메일 갈등 기록이 있습니다.",
        "Julia는 피해자의 핸드폰이 없어진 것을 처음 발견한 인물입니다."
    ]
    return hints[st.session_state.hint_count]

# ==================== 인터페이스 ====================
with st.expander("💬 용의자 심문"):
    character = st.selectbox("심문할 인물 선택", list(CHARACTER_PROMPT.keys()))
    user_input = st.text_input("이 인물에게 어떤 질문을 하시겠습니까?", key="question_input")
    if st.button("질문하기"):
        gpt_response = get_character_response(character, user_input)
        st.markdown(f"**{character}:** {gpt_response}")
        st.session_state.messages.append((character, user_input, gpt_response))

        if st.button("이 대화에서 단서를 저장하기"):
            st.session_state.clues.append(gpt_response)

with st.expander("🧩 단서 메모장"):
    if st.session_state.clues:
        for i, clue in enumerate(st.session_state.clues):
            st.markdown(f"🔎 단서 {i+1}: {clue}")
    else:
        st.write("저장된 단서가 없습니다.")

with st.expander("🧠 힌트 요청"):
    if st.session_state.hint_count < 2:
        if st.button("힌트 보기"):
            hint = get_hint()
            st.session_state.hint_count += 1
            st.markdown(f"🔍 힌트 {st.session_state.hint_count}: {hint}")
    else:
        st.warning("힌트는 최대 2개까지만 제공됩니다.")

# ==================== 최종 추리 제출 ====================
st.markdown("---")
st.subheader("🔍 최종 추리")

with st.form("final_guess"):
    suspect = st.radio("범인은 누구라고 생각하십니까?", list(CHARACTER_PROMPT.keys()))
    motive = st.text_input("동기는 무엇인가요?")
    method = st.text_input("범행 수단은 무엇인가요?")
    submitted = st.form_submit_button("제출하기")

    if submitted:
        is_correct = ("Mark" in suspect and "돈" in motive and ("약" in method or "독" in method))
        if is_correct:
            st.success("🎯 정답입니다! 사건의 진실을 정확히 밝혀냈습니다.")
        else:
            st.error("❌ 추리가 틀렸습니다. 하지만 훌륭한 시도였습니다.")
        st.markdown("### 📄 탐정 보고서")
        st.markdown(f"""
- **선택한 범인**: {suspect}  
- **동기**: {motive}  
- **방법**: {method}  
- **단서 수**: {len(st.session_state.clues)}  
- **사용한 힌트 수**: {st.session_state.hint_count}  
- **제출 시각**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")
