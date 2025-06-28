import streamlit as st

# ======================== 초기 설정 =========================
st.set_page_config(page_title="ChatCrime: 대화 속에 답이 있다", layout="wide")

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
if "selected_character" not in st.session_state:
    st.session_state.selected_character = "조수"

# ======================== 캐릭터 목록 =========================
characters = {
    "👧 지은": "지은",
    "👦 민수": "민수",
    "🧒 수빈": "수빈",
    "🕵️ 조수": "조수"
}

# ======================== 단서 사이드바 =========================
st.sidebar.title("🧩 단서 보기")
clues = [
    "🧀 피자에는 민경이 못 먹는 고르곤졸라가 있었다.",
    "🕒 사망 추정 시각은 오후 3시경.",
    "📱 민경 휴대폰엔 수빈과 격한 문자 흔적.",
    "🍷 와인잔 하나는 깨져 있었고, 흔적은 닦여 있었다.",
    "🚪 문은 잠겨 있지 않았고, 초인종은 고장 나 있었다."
]
for i, clue in enumerate(clues, 1):
    with st.sidebar.expander(f"단서 {i}", expanded=False):
        st.markdown(clue)

# ======================== 대화 주제 및 선택 =========================
st.title("💬 ChatCrime: 대화 속에 답이 있다")
st.markdown("**👆 왼쪽에서 단서를 확인하고, 아래에서 인물과 질문을 선택해보세요.**")

cols = st.columns(len(characters))
for i, (label, name) in enumerate(characters.items()):
    if cols[i].button(label):
        st.session_state.selected_character = name

st.markdown(f"**🎯 현재 선택된 인물: `{st.session_state.selected_character}`**")

# ======================== 질문 입력 =========================
question = st.text_input("💬 어떤 질문을 할까요?", placeholder="예: 오늘 오후에 어디 있었나요?")

if question:
    role = st.session_state.selected_character
    st.session_state.chat_log.append(("user", f"[{role}] {question}"))

    # ======================== 응답 생성 (간이 룰베이스) =========================
    if role == "지은":
        answer = "민경이와는 사이 좋았어요... 요즘 고민이 많아 보였지만요."
    elif role == "민수":
        answer = "최근에 다퉜지만, 화해하려고 간 거예요. 그날은 조용했어요."
    elif role == "수빈":
        answer = "언니랑 말 못할 일이 있었어요. 하지만 이런 일은 원치 않았어요."
    elif role == "조수":
        answer = "이번 단서들을 보면 오후 3시 전후로 사건이 벌어진 듯해요. 추가 조사 필요합니다."
    else:
        answer = "아직 알 수 없습니다."

    st.session_state.chat_log.append(("bot", f"[{role}] {answer}"))

# ======================== 대화 로그 출력 =========================
for sender, msg in st.session_state.chat_log:
    with st.chat_message("user" if sender == "user" else "assistant"):
        st.markdown(msg)
