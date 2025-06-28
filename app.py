# ChatCrime: Streamlit-based Multi-Character Murder Mystery Game (Updated)

import streamlit as st
from PIL import Image

st.set_page_config(page_title="ChatCrime: 대화 속에 답이 있다", layout="wide")

# ============================ 캐릭터 초기 설정 ============================
characters = {
    "지은": {
        "role": "민경이의 친구",
        "personality": "침착하고 방어적이며 감정을 잘 드러내지 않음",
        "intro_react": "...말도 안 돼. 민경이가 왜 이런 일을 당한 거야?",
    },
    "수빈": {
        "role": "민경이의 아는 동생",
        "personality": "소극적이고 조심스러우며 죄책감이 있는 듯함",
        "intro_react": "...언니한테 못할 일이 있었어요. 하지만 이렇게 될 줄은 몰랐어요...",
    },
    "민호": {
        "role": "민경이의 남자친구",
        "personality": "과묵하고 자기방어가 강하며 자존심이 셈",
        "intro_react": "민경이가... 죽었다고요? 그럴 리 없어요. 어제까지 멀쩡했는데...",
    },
    "조수 탐정": {
        "role": "당신을 돕는 조수형 AI",
        "personality": "침착하고 사실 기반으로 알려주는 타입",
        "intro_react": "도움이 필요하시면 단서나 사건 개요에 대해 언제든 물어보세요.",
    }
}

# ============================ 단서 및 사건 정보 ============================
clues = [
    "피자에는 민경이 못 먹는 고르곤졸라가 있었습니다.",
    "사망 추정 시각은 오후 3시경입니다.",
    "민경 휴대폰엔 수빈과 격한 문자 흔적이 있습니다.",
    "와인잔 하나는 깨져 있었고, 흔적은 닦여 있었습니다.",
    "문은 잠겨 있지 않았고, 초인종은 고장 나 있었습니다."
]

case_info = {
    "사건 개요": "오늘 오후, 민경 씨가 자택에서 숨진 채 발견되었습니다. 집 안엔 싸운 흔적은 없지만, 단서들이 흩어져 있습니다. 총 3명의 용의자가 있으며, 이들과 이야기를 나누며 진실을 파악해야 합니다.",
    "사망 추정 시각": "오후 3시경",
    "최초 발견자": "지은",
}

# ============================ 세션 상태 초기화 ============================
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
if "selected_char" not in st.session_state:
    st.session_state.selected_char = ""

# ============================ 사이드바 - 단서 ============================
st.sidebar.markdown("## 타서 보기")
for idx, clue in enumerate(clues):
    with st.sidebar.expander(f"\ud0c0\uc11c {idx+1}"):
        st.markdown(f"{clue}")

# ============================ 상단 브리핑 ============================
st.title("🕵️ ChatCrime: \ub300\ud654 \uc18d에 \ub2f5이 \uc788\ub2e4")
st.markdown(f"**조수 탐정:** {case_info['사건 개요']}")

# ============================ 캐릭터 선택 ============================
st.markdown("### 누구에게 질문하시겠습니까?")
cols = st.columns(len(characters))
for i, (name, char) in enumerate(characters.items()):
    if cols[i].button(name):
        st.session_state.selected_char = name
        st.session_state.chat_log.append((name, char["intro_react"]))

# ============================ 대화 인터페이스 ============================
if st.session_state.selected_char:
    st.markdown(f"### 🗣️ {st.session_state.selected_char}와의 대화")
    for speaker, msg in st.session_state.chat_log:
        st.markdown(f"**{speaker}**: {msg}")

    user_input = st.text_input("무엇을 물어보시겠어요? (예: '사망 시간에 뭐 하고 있었어?')", key="user_input")

    if user_input:
        selected = st.session_state.selected_char
        reply = ""

        # 조수는 팩트 기반으로 답변
        if selected == "조수 탐정":
            if "사망" in user_input:
                reply = f"사망 추정 시각은 {case_info['사망 추정 시각']}입니다."
            elif "최초" in user_input or "누가 발견" in user_input:
                reply = f"최초 발견자는 {case_info['최초 발견자']}입니다."
            else:
                reply = "그 부분은 기록에 없습니다."

        # 캐릭터별 반응
        else:
            lowered = user_input.lower()
            if "단서" in lowered or any(x in lowered for x in ["와인", "문자", "고르곤졸라"]):
                reply = f"글쎄요... 그건 직접 확인해보셔야 하지 않을까요?"
            elif "사망" in lowered or "죽" in lowered:
                reply = f"...그날 이후로 모든 게 흐릿해요. {selected} 입장에선 아직도 믿기 힘든 일이에요."
            elif "3시" in lowered:
                reply = f"글쎄요... 그 시간엔 혼자 있었어요. 증명할 방법은 없지만..."
            else:
                reply = f"그건 잘 모르겠어요."

        st.session_state.chat_log.append(("나", user_input))
        st.session_state.chat_log.append((selected, reply))
