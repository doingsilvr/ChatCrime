# ChatCrime v2.4 - 사용자 메모장 + 용의자 감정 캐릭터 강화
import streamlit as st
import openai

# Streamlit 기본 설정
st.set_page_config(page_title="ChatCrime", layout="wide")
st.title("🕵️ ChatCrime: 대화 속에 답이 있다")

# OpenAI API 초기화
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "hint_count" not in st.session_state:
    st.session_state.hint_count = 0
if "briefing_done" not in st.session_state:
    st.session_state.briefing_done = False
if "notepad" not in st.session_state:
    st.session_state.notepad = ""

# 캐릭터 정의 + 감정 캐릭터
CHARACTERS = {
    "지은 (친구)": {
        "description": "당신은 피해자의 친구 지은입니다. 평소 명랑하지만 최근 소원해졌습니다. 겉으로는 밝게 웃지만 속마음은 복잡하며, 감정적으로 방어적입니다.",
        "avatar": "🙂",
        "tone": "말투는 명랑하고 덤덤하지만, 민감한 질문에는 살짝 불편한 기색을 내비칩니다."
    },
    "민수 (남자친구)": {
        "description": "당신은 피해자의 남자친구 민수입니다. 자존심이 강하고 냉정한 스타일이며, 탐정의 질문에 논리적으로 대응하려 하지만 감정이 격해질 때가 있습니다.",
        "avatar": "😠",
        "tone": "말투는 차분하려 하지만 가끔 격해지며, 부정적인 질문엔 방어적으로 반응합니다."
    },
    "수빈 (아는 동생)": {
        "description": "당신은 피해자의 아는 동생 수빈입니다. 내성적이며 주눅 든 태도를 보이지만, 감정이 자극되면 감정을 억누르지 못합니다.",
        "avatar": "😐",
        "tone": "소극적인 말투지만, 몰아붙이면 감정이 격해져 버벅이거나 분노를 보입니다."
    }
}

# 단서 (힌트) 리스트
HINTS = [
    "📷 민수가 사건 전날 밤 11시 피해자 집에 방문한 CCTV 기록.",
    "📱 피해자와 민수 사이 격한 문자 내역.",
    "💬 친구들 증언 - 지은과 피해자 말다툼 정황.",
    "🧾 수빈의 금전적 부탁 거절 관련 이야기.",
    "🧴 바닥에 엎질러진 물병에서 약물 흔적.",
    "🍕 피해자만 먹은 피자에서 약물 검출 가능성. (사망 원인 핵심 단서)"
]

# GPT 응답 생성 함수
def get_character_response(character, user_input):
    desc = CHARACTERS[character]["description"]
    tone = CHARACTERS[character]["tone"]
    prompt = f"""
당신은 '{character}' 역할을 맡은 AI입니다.
- {desc}
- 감정 스타일: {tone}
- 초기에는 자신의 결점이나 갈등은 숨기려 하지만, 탐정이 단서를 제시하면 감정을 드러내며 진실을 털어놓습니다.
- 자연스럽고 감정 표현이 풍부한 말투로 대화하십시오.

탐정의 질문: "{user_input}"
{character}:
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 사건 브리핑
def show_briefing():
    with st.chat_message("assistant", avatar="📁"):
        st.markdown("""
**[비서 AI]**
안녕하세요 탐정님. 사건 개요를 보고드립니다.

오늘 아침 피해자는 **자택 거실에서 의식을 잃은 채 발견**되었습니다. 외부 침입 흔적은 없으며, 함께 있던 세 명의 지인들이 현재 용의자로 조사받고 있습니다.

- **지은**: 친구
- **민수**: 남자친구
- **수빈**: 아는 동생

식탁 위에는 피해자만 먹은 **피자 조각**이 남겨져 있었고, 현재 **음식물 내 약물 중독**이 사망 원인으로 지목되고 있습니다.

🔍 단서는 **오른쪽의 힌트 버튼**을 누를 때마다 하나씩 공개됩니다. (총 6개)
🗒️ 하단의 메모장을 활용해 수사 기록을 정리할 수 있습니다.
""")

# 브리핑 표시
if not st.session_state.briefing_done:
    show_briefing()
    st.session_state.briefing_done = True

# 사용자 입력
character = st.selectbox("💬 누구에게 질문하시겠습니까?", list(CHARACTERS.keys()))
user_input = st.chat_input("질문을 입력하세요")

# 이전 대화 렌더링
for msg in st.session_state.messages:
    role = msg["role"]
    name = msg["name"]
    avatar = CHARACTERS[name]["avatar"] if role == "assistant" else "🕵️"
    with st.chat_message(role, avatar=avatar):
        st.markdown(f"**{name}**: {msg['content']}")

# 질문 처리
if user_input:
    st.session_state.messages.append({"role": "user", "name": "탐정", "content": user_input})
    with st.chat_message("user", avatar="🕵️"):
        st.markdown(f"**탐정**: {user_input}")

    gpt_response = get_character_response(character, user_input)
    st.session_state.messages.append({"role": "assistant", "name": character, "content": gpt_response})
    with st.chat_message("assistant", avatar=CHARACTERS[character]["avatar"]):
        st.markdown(f"**{character}**: {gpt_response}")

# 사이드바 기능
with st.sidebar:
    st.header("🧰 조사 도구")

    if st.session_state.hint_count < len(HINTS):
        if st.button(f"🧠 힌트 요청 ({len(HINTS) - st.session_state.hint_count}개 남음)"):
            hint = HINTS[st.session_state.hint_count]
            st.session_state.hint_count += 1
            st.info(hint)
    else:
        st.info("모든 힌트를 다 확인하셨습니다.")

    if st.button("🧩 최종 추리 제출"):
        st.markdown("👉 추리 제출 기능은 추후 업데이트될 예정입니다.")

# 사용자 메모장
st.markdown("---")
st.subheader("🗒️ 수사 메모장")
st.session_state.notepad = st.text_area("자유롭게 수사 노트를 작성하세요:", value=st.session_state.notepad, height=200)

