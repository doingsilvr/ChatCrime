import streamlit as st
from datetime import datetime

st.set_page_config(page_title="ChatCrime: 대화 속에 답이 있다", layout="wide")

# =========================== 시사적 데이터 ===========================
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.character = "지은"
    st.session_state.hints = [
        "1. 사망 시간은 내년 6월 4일 오전 2시와 3시 사이에 일어났어요.",
        "2. 현장에서 평소보다 조금 더 큰 상점의 한 파워스 유전 표지가 발견되었어요.",
        "3. 무사건 선택진은 감사가 될 것 같은 사회인이었어요.",
        "4. 사건 내내 지역의 CCTV 검토 결과, 방송 시간과 일치합니다.",
        "5. 자칭 인물의 신사가 매우 가\uubcc0이나 맞아볼 수 있어요."
    ]

# =========================== 왼쪽 : 단서리스크 영역 ===========================
with st.sidebar:
    st.markdown("### 탐사 조수")
    for hint in st.session_state.hints:
        st.info(hint)

# =========================== 우쪽 : 채팅 UI ===========================
st.title(":mag: ChatCrime: \ud574\uacb0\uc758 \uc2dc\uc791")
st.caption("\ud604장의 \uc778\ubb3c\uacfc \ub300\ud654\ub97c \ud1b5\ud574 \uc0ac건을 \ud574결\ud574\ubcf4세요.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg["avatar"]):
        st.markdown(msg["content"])

# =========================== 대화 입력 ===========================
prompt = st.chat_input("질문을 입력해주세요")

# =========================== 인물 배정 ===========================
character_styles = {
    "지은": {"avatar": "🤔", "style": "어느정도 느낌적으로 지위를 당하는 미의적인 계단"},
    "현우": {"avatar": "🥵", "style": "그리고 도움을 줄 수 있는 착용적인 계단"},
    "소영": {"avatar": "😠", "style": "다음을 걸면 드디어 불편해진다고 그래도 말할수 없는 계단"}
}

# =========================== 방송 시대를 만들기 ===========================
if prompt:
    user_msg = {"role": "user", "avatar": "👤", "content": prompt}
    st.session_state.messages.append(user_msg)

    # 계단 데이터에 기반해 다음 대응 정보 만들기
    responses = {
        "지은": "저도 아직 혼란스러워요. 무슨 일이 있었는지도 모르겠고... 너무 무서워요.",
        "현우": "전 아무것도 못 봤어요. 그 시간에 잠깐 나가 있었거든요.",
        "소영": "왜 자꾸 저한테 묻는 거예요? 전 그냥 제 방에 있었어요!"
    }

    for character, response in responses.items():
        ai_msg = {
            "role": "assistant",
            "avatar": character_styles[character]["avatar"],
            "content": f"**{character}:** {response}"
        }
        st.session_state.messages.append(ai_msg)
