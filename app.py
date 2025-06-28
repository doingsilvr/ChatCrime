import streamlit as st
from datetime import datetime
import random

# ===================== 초기 설정 =====================
st.set_page_config(page_title="ChatCrime: 대화 속에 답이 있다", layout="wide")
st.title("🕵️ ChatCrime: 대화 속에 답이 있다")

# ===================== 세션 초기화 =====================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "hint_index" not in st.session_state:
    st.session_state.hint_index = -1
if "current_suspect" not in st.session_state:
    st.session_state.current_suspect = ""

# ===================== 캐릭터 설정 =====================
CHARACTER_PROMPTS = {
    "지은": """
너는 민경의 친구 지은이야. 겉보기에는 활발하지만, 요즘 민경과의 관계가 흔들리고 있었어.
갑작스러운 죽음에 충격을 받았고, 평소 밝은 너도 무너지는 중이야.
처음 대화에선 "민경이가 죽었다니 믿기지가 않아요.."라고 말해.
질문을 받기 전, 감정 섞인 짧은 말을 먼저 해. 너무 쉽게 용의자로 지목되지 않으려 해.
단서를 보여주면 점점 진실을 털어놓게 돼.
""",
    "민수": """
너는 민경의 남자친구 민수야. 겉보기엔 조용하고 신사적이지만 감정 기복이 커.
죽음에 충격을 받아 말을 잇지 못하는 상태야. 처음에는 "민경아... 민경아..."라고 중얼거려.
단서를 보면 감정이 폭발하고 사실을 고백할 수도 있어.
""",
    "수빈": """
너는 민경의 아는 동생 수빈이야. 평소에 친하게 지냈지만, 집안 문제로 멀어진 적 있어.
죽음에 놀라고 있고, 자책감도 조금 있어. 처음엔 "언니가 죽은 게 맞아요...? 어쩌다가 그런 거죠?"라고 말해.
단서를 보면 거짓말을 들키지 않기 위해 불안해져.
"""
}

FIRST_LINES = {
    "지은": "민경이가 죽었다니 믿기지가 않아요..",
    "민수": "민경아... 민경아...",
    "수빈": "언니가 죽은 게 맞아요...? 어쩌다가 그런 거죠?"
}

HINTS = [
    "🧾 단서 1: 민경의 혈액에서 미세한 독극물 성분 검출됨",
    "📱 단서 2: 지은과 민경의 최근 문자에서 다툰 흔적 확인",
    "🧣 단서 3: 민수의 옷에서 피자 소스 얼룩 발견됨",
    "💬 단서 4: 수빈이 민경의 방에 무단 침입한 기록 있음"
]

# ===================== 좌측 사이드바 (사건 개요 / 힌트 / 메모) =====================
with st.sidebar:
    st.header("🕵️ 사건 개요")
    st.markdown("""
한적한 주택가에서 벌어진 사망 사건. 피해자 민경은 피자를 먹은 직후 의식을 잃고 사망.
현장에는 친구 지은, 남자친구 민수, 아는 동생 수빈이 함께 있었음.
세 인물은 서로 다른 진술을 하고 있으며, 단서들을 종합해 진실을 파악해야 함.
""")

    st.divider()
    st.subheader("🔍 단서 보기")
    if st.button("힌트 보기"):
        if st.session_state.hint_index + 1 < len(HINTS):
            st.session_state.hint_index += 1

    for i in range(st.session_state.hint_index + 1):
        st.markdown(HINTS[i])

    st.divider()
    st.subheader("📝 메모")
    st.text_area("추리 기록을 남겨보세요", key="memo")

# ===================== 캐릭터 선택 =====================
st.markdown("#### 💬 누구에게 질문하시겠습니까?")
suspect = st.selectbox("", ["지은(친구)", "민수(남자친구)", "수빈(아는 동생)"])
st.session_state.current_suspect = suspect.split("(")[0]

# ===================== 대화 영역 =====================
with st.chat_message("assistant", avatar="🕵️"):
    st.markdown("안녕하세요. 사건을 해결하려면 인물들과의 대화가 필요합니다. 질문을 입력해보세요.")

selected = st.session_state.current_suspect

# 첫 대화 삽입
if not any(m["name"] == selected for m in st.session_state.messages):
    st.session_state.messages.append({
        "role": "character",
        "name": selected,
        "content": FIRST_LINES[selected]
    })

# 기존 메시지 출력
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    elif msg["role"] == "character":
        with st.chat_message(msg["name"], avatar="😐"):
            st.markdown(f"**{msg['name']}**: {msg['content']}")

# ===================== 사용자 입력 =====================
if prompt := st.chat_input("질문을 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 캐릭터 응답 생성 (모의 프롬프트)
    prompt_text = f"""
{CHARACTER_PROMPTS[selected]}

탐정: {prompt}
{selected}의 대답:
"""

    # 실제 GPT 응답을 넣는다면 여기에 모델 호출
    import random
    dummy_response = random.choice([
        "그건... 제가 일부러 그런 건 아니에요. 민경이랑은 그저... 가끔 다툰 적은 있었지만.",
        "저도 아직 혼란스러워요. 무슨 일이 있었는지도 모르겠고... 너무 무서워요.",
        "사실은 그날, 저 혼자 피자를 만들었어요. 근데 그 안에 뭐가 들어 있었는지는 저도 몰랐어요.",
    ])

    st.session_state.messages.append({
        "role": "character",
        "name": selected,
        "content": dummy_response
    })

    st.rerun()
