import streamlit as st
import openai

# ==================== 초기 설정 ====================
st.set_page_config(page_title="ChatCrime", layout="wide")
st.title("🕵️ ChatCrime: 대화 속에 답이 있다")

# ==================== API 키 로딩 ====================
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ==================== 세션 상태 초기화 ====================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "clues" not in st.session_state:
    st.session_state.clues = []
if "hint_count" not in st.session_state:
    st.session_state.hint_count = 0

# ==================== 캐릭터 프롬프트 ====================
CHARACTER_PROMPT = {
    "Ellen (큐레이터)": "당신은 피해자의 동료 큐레이터 엘렌입니다. 이성적이고 방어적이며 피해자와 최근 갈등이 있었습니다.",
    "Mark (사진작가)": "당신은 감정 기복이 심한 사진작가 마크입니다. 피해자와 돈 문제로 갈등이 있었고, 공격적인 반응을 보이기도 합니다.",
    "Julia (청소직원)": "당신은 조용한 청소 직원 줄리아입니다. 피해자를 가장 먼저 발견했으며, 말수가 적고 소극적으로 응답합니다."
}

# ==================== 힌트 제공 함수 ====================
def get_hint():
    hints = [
        "📷 CCTV에는 Mark가 사건 당일 늦게까지 갤러리에 머문 장면이 포착되었습니다.",
        "📩 Ellen과 피해자 사이에는 작품 소유권을 두고 갈등이 있었던 이메일이 발견되었습니다.",
        "📱 Julia는 피해자의 핸드폰이 없어진 것을 가장 먼저 발견했습니다."
    ]
    return hints[st.session_state.hint_count]

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

# ==================== 사건 개요 ====================
with st.expander("📁 사건 개요"):
    st.markdown("""
🖼️ 도심의 갤러리에서 한 남성이 의식을 잃은 채 발견되었다. 외부 침입 흔적은 없었고, 현장에 남아있던 인물은 단 세 명.  
누가, 왜, 어떻게 이런 일이 벌어진 것일까?  
당신은 AI 탐정. 그들과 대화하며 진실을 밝혀야 한다.

💡 **힌트는 단 2회만 요청할 수 있습니다.**
    """)

# ==================== 채팅창 UI ====================
character = st.selectbox("💬 누구에게 질문하시겠습니까?", list(CHARACTER_PROMPT.keys()))
user_input = st.chat_input("질문을 입력하세요")

# 이전 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(f"**{msg['name']}**: {msg['content']}")

# 새 질문 처리
if user_input:
    st.session_state.messages.append({"role": "user", "name": "탐정", "content": user_input})
    with st.chat_message("user"):
        st.markdown(f"**탐정**: {user_input}")

    gpt_response = get_character_response(character, user_input)
    st.session_state.messages.append({"role": "assistant", "name": character, "content": gpt_response})
    with st.chat_message("assistant"):
        st.markdown(f"**{character}**: {gpt_response}")

# ==================== 우측 사이드바 도구 ====================
with st.sidebar:
    st.header("🧰 조사 도구")

    if st.button("📌 마지막 응답 메모하기"):
        if st.session_state.messages:
            last_response = st.session_state.messages[-1]["content"]
            st.session_state.clues.append(last_response)
            st.success("단서를 메모에 저장했습니다.")
        else:
            st.warning("저장할 응답이 없습니다.")

    if st.session_state.hint_count < 2:
        if st.button(f"🧠 힌트 요청 ({2 - st.session_state.hint_count}회 남음)"):
            hint = get_hint()
            st.session_state.hint_count += 1
            st.info(hint)
    else:
        st.info("더 이상 힌트를 사용할 수 없습니다.")

    if st.button("🧩 최종 추리 제출"):
        st.markdown("👉 추리 제출은 아직 연결되지 않았습니다. 추후 업데이트 예정입니다.")
