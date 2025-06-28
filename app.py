from datetime import datetime
import streamlit as st
import random
import uuid

# ============================ 기본 설정 ============================
st.set_page_config(page_title="ChatCrime: 대화 속에 답이 있다", layout="wide")

if "turn_count" not in st.session_state:
    st.session_state.turn_count = 0
if "messages" not in st.session_state:
    st.session_state.messages = []
if "suspect" not in st.session_state:
    st.session_state.suspect = "지은"
if "memo" not in st.session_state:
    st.session_state.memo = ""
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# ============================ 캐릭터 프롬프트 ============================
character_profiles = {
    "지은": "밝고 명랑한 성격이지만 최근엔 감정 기복이 있으며, 질문에는 성실히 답하려 함. 범인으로 오해받을 만한 정황은 숨기려 함.",
    "수빈": "순박하고 감정 표현이 풍부함. 솔직한 편이나, 불리한 정보는 얼버무리려 함.",
    "민수": "말수가 적고 방어적인 태도. 감정 기복은 적으나 핵심을 말하는 걸 피하는 경향이 있음."
}

# ============================ 단서 목록 ============================
clues = [
    "📌 단서 1: 피자 박스에서 파란색 가루가 검출됨. 감식 결과, 이는 일반 조미료가 아닌 독성 성분일 가능성이 있음.",
    "📌 단서 2: 사건 당일 정전이 있었음. 지은은 TV를 보고 있었다고 했지만, 당시 TV는 작동할 수 없었음.",
    "📌 단서 3: 민수는 사건 30분 전까지 민경과 격한 문자 대화를 나눈 기록이 있음.",
    "📌 단서 4: 수빈은 부엌 청소 담당이었지만, 사건 당일 청소를 하지 않았고 피자 재료 일부가 사라졌다고 진술함.",
    "📌 단서 5: 피자 반죽에는 평소와 다른 브랜드의 치즈가 사용되었음."
]

# ============================ 캐릭터 응답 샘플 ============================
responses = {
    "지은": [
        "믿기지 않아요... 민경이가 그런 일을 당하다니...",
        "전 그냥 TV를 보고 있었어요. 그 시간에 무슨 일이 있었는지 몰라요...",
        "제가 왜 그런 짓을 하겠어요? 민경이랑은... 최근에 사이가 조금 멀어지긴 했지만, 그런 건 흔한 일이잖아요?"
    ],
    "수빈": [
        "언니가... 진짜 죽은 거예요? 어떻게 그런 일이...",
        "사실 부엌 청소는 못 했어요. 너무 피곤해서... 근데 전 진짜 아무것도 몰라요!",
        "그날은 이상했어요. 재료 몇 개가 사라진 것도 같고... 누가 가져간 걸까요?"
    ],
    "민수": [
        "......민경아...",
        "저랑은 별일 없었어요. 그냥 평소처럼요.",
        "문자요? 그냥 다툼이 좀 있었던 거지, 그게 무슨 큰일이라고..."
    ]
}

# ============================ 조수 AI ============================
def show_assistant(turn):
    index = (turn // 5) - 1
    if 0 <= index < len(clues):
        st.chat_message("조수", avatar="🧭").write(f"🕵️‍♀️ 수사 리포트: {clues[index]}")

# ============================ UI 구성 ============================
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("### 📋 사건 개요")
    st.info("👤 피해자: 민경 (여성, 27세)\n\n🕒 발견 시각: 오후 6시경\n\n📍 장소: 집 부엌\n\n🔍 상황: 피자 조각을 들고 쓰러진 채 발견됨. 주변에 수상한 가루 흔적 존재.")

    st.markdown("---")
    st.markdown("### 📝 메모장")
    memo = st.text_area("조사 메모", value=st.session_state.memo, height=300)
    st.session_state.memo = memo

with col2:
    st.markdown("## 💬 ChatCrime: 대화 속에 답이 있다")

    suspect = st.selectbox("👤 누구에게 질문하시겠습니까?", ["지은", "수빈", "민수"], index=["지은", "수빈", "민수"].index(st.session_state.suspect))
    st.session_state.suspect = suspect

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=msg.get("avatar", None)):
            st.markdown(msg["content"])

    prompt = st.chat_input("질문을 입력하세요")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)

        st.session_state.turn_count += 1

        reply = random.choice(responses[suspect])
        avatar = {"지은": "🙂", "수빈": "😳", "민수": "😐"}[suspect]
        st.session_state.messages.append({"role": suspect, "content": f"{reply}", "avatar": avatar})
        st.chat_message(suspect, avatar=avatar).markdown(reply)

        if st.session_state.turn_count % 5 == 0:
            show_assistant(st.session_state.turn_count)

    st.rerun()
