import streamlit as st

# ======================== 초기 설정 =========================
st.set_page_config(page_title="ChatCrime: 대화 속에 답이 있다", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "briefing_done" not in st.session_state:
    st.session_state.briefing_done = False

# ======================== 사건 브리핑 =========================
briefing = """
🔍 **사건 개요**  
피해자 **민경**은 자신의 자택에서 숨진 채 발견되었습니다.  
현장에는 피자 상자, 깨진 유리잔, 다툰 흔적이 있었고,  
친구 **지은**, 남자친구 **민수**, 아는 동생 **수빈**이 차례로 집을 방문했다고 진술했습니다.

이제 이들과 대화하며 진실을 밝혀야 합니다.
"""

# ======================== 사이드바 - 단서 =========================
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

# ======================== 상단 브리핑 박스 =========================
with st.expander("🕵️ 보조 탐정의 사건 브리핑", expanded=True):
    st.markdown(briefing)

# ======================== 메인 - 대화 시작 =========================
st.title("💬 ChatCrime: 대화 속에 답이 있다")

if not st.session_state.briefing_done:
    with st.chat_message("assistant", avatar="🕵️"):
        st.markdown(briefing)
    st.session_state.briefing_done = True

# ======================== 이전 대화 출력 =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar", "")):
        st.markdown(message["content"])

# ======================== 사용자 입력창 =========================
if user_input := st.chat_input("누구에게 무엇을 물어볼까요? (예: '수빈, 오늘 무슨 일 있었어?')"):
    st.session_state.messages.append({"role": "user", "content": user_input, "avatar": "🙋‍♀️"})
    with st.chat_message("user", avatar="🙋‍♀️"):
        st.markdown(user_input)

    # 여기선 간단하게 용의자 이름 포함 여부로 답변 나눔 (추후 LLM 연동 가능)
    if "지은" in user_input:
        reply = "지은: 민경이와는 사이 좋았어요... 요즘 고민이 많아 보였지만요."
        avatar = "👧"
    elif "민수" in user_input:
        reply = "민수: 민경이랑은 최근에 다퉜지만, 그날은 그냥 화해하려고 갔어요."
        avatar = "👦"
    elif "수빈" in user_input:
        reply = "수빈: 언니한테 말 못할 일이 있었어요. 하지만 이런 일까지 벌어질 줄은..."
        avatar = "👧"
    elif "조수" in user_input or "보조" in user_input:
        reply = "보조 탐정: 단서가 새로 확보됐어요. 좌측에서 확인해보세요."
        avatar = "🕵️‍♂️"
    else:
        reply = "보조 탐정: 누구에게 질문하실 건가요? 이름을 포함해 주세요."
        avatar = "🕵️‍♂️"

    st.session_state.messages.append({"role": "assistant", "content": reply, "avatar": avatar})
    with st.chat_message("assistant", avatar=avatar):
        st.markdown(reply)
