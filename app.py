import streamlit as st
import random

st.set_page_config(page_title="ChatCrime: 대화 속에 답이 있다", layout="wide")
st.markdown("""
    <style>
        body {
            background-color: #1e1e1e;
        }
        .main {
            color: white;
        }
        .css-1lcbmhc {
            background-color: #1e1e1e;
        }
        .block-container {
            padding-top: 2rem;
        }
        .stTextInput>div>div>input {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🕵️ ChatCrime: 대화 속에 답이 있다")

# 사건 브리핑 (조수 탐정)
st.markdown("""
#### 🧾 사건 개요
오늘 오후, 민경 씨가 자택에서 숨진 채 발견되었습니다. 집 안에는 외부 침입의 흔적은 없었지만, 단서들이 흩어져 있었고, 방 안에는 감정의 잔상이 남겨져 있었습니다. 

민경은 평소 친구들과는 밝게 지냈지만, 최근 고민이 많아 보였다고 합니다. 그리고... 그녀와 얽힌 복잡한 감정의 실타래 속에 얽힌 세 사람이 있습니다. 

당신은 이들과 대화하며, 감정의 파편 속에서 진실을 찾아야 합니다.
""")

st.divider()
st.subheader("누구에게 질문하시겠습니까?")
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    selected_character = st.radio("", ["지은", "수빈", "민호", "조수 탐정"], label_visibility="collapsed")

# 단서 리스트 UI
with col4:
    clue = st.selectbox("단서 보기", ["단서 1", "단서 2", "단서 3", "단서 4", "단서 5"])

# 단서 내용 정의
clue_details = {
    "단서 1": "민경의 휴대폰 잠금 화면에 '지은이 나한텐 다 말해줬어'라는 메시지가 도착해 있었다.",
    "단서 2": "부엌 싱크대 안쪽에서 깨진 유리 조각과 붉은 얼룩이 발견되었다.",
    "단서 3": "수빈의 방 서랍에서 민경의 것으로 추정되는 일기장이 발견되었다.",
    "단서 4": "민호가 당일 오후 2시경 민경의 집 근처를 지나간 CCTV가 확인되었다.",
    "단서 5": "사망 시각 추정은 오후 3시경이며, 문은 안에서 잠겨 있었다."
}

with st.expander(f"🔍 {clue} 열기"):
    st.markdown(clue_details[clue])

st.divider()

# 대화 상태 저장
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# 캐릭터별 응답 정의
def respond(character, user_input):
    user_input = user_input.lower()
    if character == "조수 탐정":
        if "브리핑" in user_input:
            return "[조수] 이번 단서들을 보면 오후 3시 전후로 사건이 벌어진 듯해요. 추가 조사 필요합니다."
        elif "최초 발견자" in user_input:
            return "[조수] 최초 발견자는 민경 씨의 친구 지은입니다."
        elif "사망 시각" in user_input:
            return "[조수] 부검 결과, 사망 시각은 오후 3시 전후로 추정됩니다."
        else:
            return "[조수] 도움이 필요하시면 단서나 사건 개요에 대해 언제든 물어보세요."

    if character == "지은":
        if "민경" in user_input:
            return "...말도 안 돼. 민경이가 왜 이런 일을 당한 거야?"
        elif "단서 1" in user_input:
            return "그 메시지... 내가 보낸 거 아니야. 나도 그거 보고 깜짝 놀랐어."
        elif "단서 5" in user_input:
            return "그 시간엔... 나는 집에 있었어. 민경이랑 연락도 안 됐고."
        else:
            return "그건 잘 모르겠어..."

    if character == "수빈":
        if "민경" in user_input:
            return "민경이는... 요즘 고민이 많아 보였어요. 가끔 울고 있었고."
        elif "단서 3" in user_input:
            return "일기장... 그건 제가 보관해달라는 부탁을 받은 거예요. 절대 훔친 거 아니에요."
        elif "단서 5" in user_input:
            return "그 시간에 저는 카페에 있었어요. 영수증도 있어요."
        else:
            return "죄송해요. 그건 잘 모르겠어요."

    if character == "민호":
        if "민경" in user_input:
            return "민경이랑은... 요즘 말이 잘 안 통했어. 근데 이건 아니지."
        elif "단서 4" in user_input:
            return "맞아, 그 근처 지났어. 근데 들어가진 않았어. 그냥 우연이야."
        elif "단서 5" in user_input:
            return "오후 3시? 그때 난 집에 있었어. 아무도 증명 못 하겠지만."
        else:
            return "나도 그건 몰라."

    return "...무슨 말인지 잘 모르겠어."

# 채팅 영역 표시
st.subheader(f"🗣️ {selected_character}와의 대화")
for msg in st.session_state.chat_log:
    st.markdown(f"**{msg['role']}**: {msg['message']}")

# 사용자 입력창
user_input = st.text_input("무엇을 물어보시겠어요? (예: '사망 시간에 뭐 하고 있었어?')", key="input")
if st.button("전송"):
    if user_input:
        response = respond(selected_character, user_input)
        st.session_state.chat_log.append({"role": "user", "message": f"[{selected_character}] {user_input}"})
        st.session_state.chat_log.append({"role": "bot", "message": response})
        st.experimental_rerun()
