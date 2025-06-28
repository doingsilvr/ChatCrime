import streamlit as st

# ------------------ 설정 ------------------
st.set_page_config(page_title="ChatCrime", layout="wide")
st.title("🔎 ChatCrime: 대화 속에 답이 있다")

# 세션 상태 초기화
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
if "shown_briefing" not in st.session_state:
    st.session_state.shown_briefing = False

# ------------------ 사건 브리핑 ------------------
briefing = """
🔍 **사건 개요**  
피해자 **민경**은 자신의 자택에서 숨진 채 발견되었습니다.  
현장에서는 피자 상자, 깨진 유리잔, 그리고 다툰 흔적이 발견되었습니다.  
당시 현장에는 친구 **지은**, 남자친구 **민수**, 아는 동생 **수빈**이 있었으며,  
모두 ‘우연히’ 방문했다고 진술하고 있습니다.

보조 탐정: “당신은 이번 사건의 AI 수사관입니다.  
이제 용의자들과 대화를 시작해 진실을 밝혀주세요.”  
"""

# ✅ ① 상단에 고정 박스(expander)
with st.expander("🕵️‍♂️ 보조 탐정의 사건 브리핑", expanded=True):
    st.markdown(briefing)

# ✅ ② 채팅 말풍선으로 대화 시작 시 안내
if not st.session_state.get("briefing_done"):
    with st.chat_message("assistant", avatar="🕵️‍♂️"):
        st.markdown(briefing)
    st.session_state["briefing_done"] = True


# ------------------ 단서 목록 ------------------
clues = {
    "단서 1. 피자 상자": "사건 현장에 있던 피자 상자는 오후 6시 38분에 주문되었고, 주문자 이름은 '은비 친구'로 되어 있었습니다.",
    "단서 2. 유리 조각": "현관 앞에는 남성용 스마트워치 유리 조각이 있었고, 시계는 6시 40분에 멈춰 있었습니다.",
    "단서 3. CCTV 로그": "CCTV에는 6시 15분경 지민이 초인종을 누르는 장면만 있고, 나가는 장면은 없습니다.",
    "단서 4. 피해자 메모": "피해자의 휴대폰 메모장에는 '다신 이런 일 없다고 믿고 싶은데…'라는 문장이 적혀 있었습니다.",
    "단서 5. 냉장고 메모": "'금요일 저녁엔 나랑 보기로 했잖아. 다른 사람 또 불렀으면 진짜 실망이야.' 라는 메모가 붙어 있었고, 필체는 남성 것으로 추정됩니다."
}

# ------------------ 용의자 반응 ------------------
character_responses = {
    "유진": {
        "단서 1. 피자 상자": "어..? 나 말고 다른 친구 이름으로 시켰나...? 기억 안 나네~",
        "단서 2. 유리 조각": "시계요? 전혀 몰랐어요~ 저는 도착도 못 했거든요!",
        "단서 3. CCTV 로그": "지민이 왔었어? 진짜? 몰랐네~ 하하…",
        "단서 4. 피해자 메모": "음… 누구 얘기하는 건지 모르겠네요. 예전 일 아닐까요?",
        "단서 5. 냉장고 메모": "그거… 현수가 쓴 걸 수도 있겠네요. 요즘 좀 예민하긴 했어요."
    },
    "현수": {
        "단서 1. 피자 상자": "나 그런 이름으로 주문한 적 없어. 믿어줘.",
        "단서 2. 유리 조각": "시계? 내가 최근에 잃어버린 시계가 있긴 한데… 우연이겠지.",
        "단서 3. CCTV 로그": "지민이 왔었다고…? 왜 아무 말도 안 했지 그럼?",
        "단서 4. 피해자 메모": "…그건 나한테 한 말 아냐. 나 그런 짓 안 해.",
        "단서 5. 냉장고 메모": "…내 글씨 아닐 수도 있어. 누가 흉내 낸 걸 수도 있잖아."
    },
    "지민": {
        "단서 1. 피자 상자": "그… 그거 내가 주문한 건 맞는데, 그냥 같이 먹으려고요…!",
        "단서 2. 유리 조각": "시계요? 저 그런 거 안 차요! 진짜요!",
        "단서 3. CCTV 로그": "나간 장면이 없다고요? 그, 그건 이상하네요. 분명 나갔는데…",
        "단서 4. 피해자 메모": "음… 저랑 상관 없는 얘기 같아요.",
        "단서 5. 냉장고 메모": "저… 남자 아니잖아요. 전 아니에요."
    }
}

# ------------------ 사이드바 단서 ------------------
st.sidebar.title("🧩 단서 보기")
selected_clue = st.sidebar.radio("단서를 클릭해 확인하세요:", list(clues.keys()))
st.sidebar.markdown(f"**📌 단서 내용:**\n\n{clues[selected_clue]}")

# ------------------ 채팅 UI ------------------
with st.container():
    st.subheader("💬 용의자와 대화하기")
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"], avatar=msg.get("avatar", None)):
            st.markdown(msg["content"])

    user_input = st.chat_input("누구에게 무엇을 물어보시겠습니까? 예: '지민, 피자에 대해 알려줘'")
    if user_input:
        st.session_state.chat_log.append({"role": "user", "content": user_input, "avatar": "👤"})

        response = ""
        for name in character_responses:
            if name in user_input:
                for clue_title, clue_text in clues.items():
                    if any(keyword in user_input for keyword in clue_title.split()):
                        response = character_responses[name][clue_title]
                        break
                if not response:
                    response = f"{name}은(는) 잠시 생각에 잠겼습니다. 질문을 조금 더 구체적으로 해주세요."
                break
        else:
            response = "세 명 중 누구에게 질문할지 명시해 주세요. (예: '유진, 단서 3에 대해 알려줘')"

        st.session_state.chat_log.append({"role": "assistant", "content": response, "avatar": "💬"})
