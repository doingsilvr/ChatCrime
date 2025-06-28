import streamlit as st
import openai

# ==================== 기본 설정 ====================
st.set_page_config(page_title="ChatCrime", layout="wide")
st.title("🕵️ ChatCrime: 대화 속에 답이 있다")

# ==================== OpenAI 클라이언트 초기화 ====================
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==================== 세션 상태 초기화 ====================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "clues" not in st.session_state:
    st.session_state.clues = []
if "hint_count" not in st.session_state:
    st.session_state.hint_count = 0

# ==================== 캐릭터 정의 ====================
CHARACTERS = {
    "Ellen (큐레이터)": {
        "description": "당신은 피해자의 동료 큐레이터 엘렌입니다. 이성적이고 조심스러운 태도를 유지하며, 피해자와 최근 전시 주제로 갈등이 있었습니다.",
        "avatar": "🎨"
    },
    "Mark (사진작가)": {
        "description": "당신은 피해자의 친구이자 전시 참여 작가인 마크입니다. 감정 기복이 심하고, 최근 금전 문제로 피해자와 다툰 적이 있습니다.",
        "avatar": "📸"
    },
    "Julia (청소직원)": {
        "description": "당신은 조용하고 신중한 성격의 청소 직원 줄리아입니다. 사건 당일 가장 먼저 피해자를 발견했으며, 겁이 많고 말수가 적습니다.",
        "avatar": "🧹"
    }
}

# ==================== 힌트 함수 ====================
def get_hint():
    hints = [
        "📷 CCTV에는 Mark가 사건 당일 늦게까지 갤러리에 머문 장면이 포착되었습니다.",
        "📩 Ellen과 피해자 사이에는 작품 소유권을 두고 갈등이 있었던 이메일이 발견되었습니다.",
        "📱 Julia는 피해자의 핸드폰이 없어진 것을 가장 먼저 발견했습니다."
    ]
    return hints[st.session_state.hint_count]

# ==================== GPT 응답 생성 함수 ====================
def get_character_response(character, user_input):
    persona = CHARACTERS[character]["description"]
    prompt = f"""
당신은 '{character}' 역할을 맡은 AI입니다.
다음 지침을 따르세요:
- 당신은 {persona}
- 모든 답변은 탐정과 대화하듯 자연스럽고 캐릭터의 성격에 맞게 진지하게 응답하세요.
- 사실은 사실대로, 모호한 것은 모호하게 표현해도 됩니다.

탐정의 질문: "{user_input}"
{character}:"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ==================== 사건 개요 ====================
with st.expander("📁 사건 개요"):
    st.markdown("""
🖼️ 도심의 갤러리에서 한 남성이 의식을 잃은 채 발견되었습니다.  
외부 침입 흔적은 없었고, 현장에는 세 명의 인물만 있었습니다.  
당신은 AI 탐정으로서 대화를 통해 사건의 진실을 밝혀야 합니다.

👤 **용의자 관계 요약**
- **Ellen (큐레이터)**: 피해자와 갤러리를 함께 운영하던 동료
- **Mark (사진작가)**: 피해자의 친구이자 전시 참여 작가
- **Julia (청소직원)**: 사건 당일 가장 먼저 피해자를 발견한 인물

💡 **힌트는 단 2회만 요청할 수 있습니다.**
    """)

# ==================== 채팅창 UI ====================
character = st.selectbox("💬 누구에게 질문하시겠습니까?", list(CHARACTERS.keys()))
user_input = st.chat_input("질문을 입력하세요")

# ==================== 이전 대화 출력 ====================
for msg in st.session_state.messages:
    role = msg["role"]
    name = msg["name"]
    avatar = CHARACTERS[name]["avatar"] if role == "assistant" else "🕵️"
    with st.chat_message(role, avatar=avatar):
        st.markdown(f"**{name}**: {msg['content']}")

# ==================== 사용자 질문 처리 ====================
if user_input:
    st.session_state.messages.append({"role": "user", "name": "탐정", "content": user_input})
    with st.chat_message("user", avatar="🕵️"):
        st.markdown(f"**탐정**: {user_input}")

    gpt_response = get_character_response(character, user_input)
    st.session_state.messages.append({"role": "assistant", "name": character, "content": gpt_response})
    with st.chat_message("assistant", avatar=CHARACTERS[character]["avatar"]):
        st.markdown(f"**{character}**: {gpt_response}")

# ==================== 사이드 도구 UI ====================
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
        st.markdown("👉 추리 제출 기능은 추후 업데이트될 예정입니다.")
