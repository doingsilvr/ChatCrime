import streamlit as st
import pandas as pd
import datetime

# ── 페이지 설정 ──────────────────────────────────────────
st.set_page_config(
    page_title="하이오더 — 사장님 대시보드",
    page_icon="🍜",
    layout="wide",
)

# ── CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}
.block-container { padding-top: 2rem; }

/* 상단 헤더 */
.page-title { font-size: 22px; font-weight: 700; letter-spacing: -0.03em; margin-bottom: 4px; }
.page-sub   { font-size: 13px; color: #8b8fa8; margin-bottom: 20px; }

/* 스탯 카드 */
.stat-box {
    background: #ffffff;
    border: 1px solid #e8eaed;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.stat-label { font-size: 11px; color: #8b8fa8; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 6px; }
.stat-value { font-size: 26px; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 6px; }
.stat-badge-green { display:inline-block; background: rgba(45,190,122,0.1); color:#2dbe7a; font-size:11px; padding:3px 8px; border-radius:99px; font-weight:600; }
.stat-badge-yellow { display:inline-block; background: rgba(245,166,35,0.1); color:#f5a623; font-size:11px; padding:3px 8px; border-radius:99px; font-weight:600; }

/* AI 인사이트 박스 */
.insight-box {
    background: #ffffff;
    border: 1px solid rgba(0,188,212,0.2);
    border-left: 4px solid #00bcd4;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.insight-title { font-size: 11px; color: #0097a7; font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase; margin-bottom: 10px; }
.insight-row { font-size: 13px; line-height: 1.7; margin-bottom: 4px; color: #1a1a2e; }
.insight-arrow { color: #00bcd4; margin-right: 6px; }

/* 알림 배너 */
.alert-box {
    background: rgba(245,166,35,0.08);
    border: 1px solid rgba(245,166,35,0.3);
    border-radius: 10px;
    padding: 13px 18px;
    font-size: 13px;
    margin-bottom: 16px;
    line-height: 1.5;
}

/* 패널 */
.panel-title { font-size: 14px; font-weight: 700; margin-bottom: 2px; }
.panel-sub   { font-size: 11px; color: #8b8fa8; margin-bottom: 12px; }

/* 태그 */
.tag-cyan   { display:inline-block; background:rgba(0,188,212,0.1); color:#0097a7; font-size:11px; padding:2px 9px; border-radius:99px; margin:2px 2px 2px 0; border:1px solid rgba(0,188,212,0.2); }
.tag-purple { display:inline-block; background:rgba(124,77,255,0.1); color:#7c4dff; font-size:11px; padding:2px 9px; border-radius:99px; margin:2px 2px 2px 0; border:1px solid rgba(124,77,255,0.15); }

/* 문의 응답 */
.inquiry-q { font-size: 13px; margin-bottom: 7px; }
.inquiry-a {
    background: #f5f6f8;
    border: 1px solid #e8eaed;
    border-radius: 8px;
    padding: 9px 12px;
    font-size: 12px;
    color: #8b8fa8;
    line-height: 1.6;
    margin-bottom: 14px;
}
.ai-badge { display:inline-block; background:rgba(0,188,212,0.1); color:#0097a7; font-size:10px; font-weight:700; padding:2px 6px; border-radius:4px; margin-right:8px; }

/* 구분선 */
hr { border: none; border-top: 1px solid #e8eaed; margin: 12px 0; }
</style>
""", unsafe_allow_html=True)

# ── 사이드바 ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
        <div style="background:#00bcd4; color:#fff; font-weight:700; font-size:13px; border-radius:8px; width:32px; height:32px; display:flex; align-items:center; justify-content:center;">하이</div>
        <span style="font-size:16px; font-weight:700; color:#1a1a2e;">하이오더</span>
    </div>
    <div style="font-size:11px; color:#8b8fa8; margin-bottom:20px;">사장님 운영 대시보드</div>
    <div style="background:rgba(0,188,212,0.06); border:1px solid rgba(0,188,212,0.15); border-radius:10px; padding:11px 14px; margin-bottom:20px;">
        <div style="font-size:13px; font-weight:600; margin-bottom:3px;">맛집헌터 강남점</div>
        <div style="font-size:11px; color:#2dbe7a;">● 영업 중 · 테이블 8/12</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "메뉴",
        ["◈  대시보드", "◎  메뉴 관리", "✦  AI 추천 설정"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='margin:20px 0;'>", unsafe_allow_html=True)
    now = datetime.datetime.now().strftime("%H:%M")
    st.markdown(f"<div style='font-size:11px; color:#8b8fa8; text-align:center;'>현재 시각 {now}</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════
# 대시보드
# ════════════════════════════════════════════
if page == "◈  대시보드":

    st.markdown('<div class="page-title">오늘의 운영 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-sub">2025년 3월 21일 금요일 — 저녁 피크타임</div>', unsafe_allow_html=True)

    # 알림
    st.markdown("""
    <div class="alert-box">
        ⚡ <strong style="color:#f5a623;">AI 알림:</strong>
        곱창 폭탄 쌀국수 재고 부족 감지 — 주방 확인 후 품절 처리를 권장합니다
    </div>
    """, unsafe_allow_html=True)

    # 스탯 4개
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="stat-box"><div class="stat-label">오늘 매출</div><div class="stat-value">₩847K</div><div class="stat-badge-green">▲ 12% 어제 대비</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="stat-box"><div class="stat-label">총 주문수</div><div class="stat-value">63</div><div class="stat-badge-green">▲ 8건 어제 대비</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="stat-box"><div class="stat-label">AI 응답 문의</div><div class="stat-value">18</div><div class="stat-badge-green">자동 처리 100%</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="stat-box"><div class="stat-label">품절 메뉴</div><div class="stat-value" style="color:#f5a623;">2</div><div class="stat-badge-yellow">⚠ 처리 필요</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # AI 인사이트
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">✦ AI 운영 인사이트</div>
        <div class="insight-row"><span class="insight-arrow">→</span>지금 시간대(17–19시) <strong>하노이 분짜</strong> 주문이 평소 대비 2.3배 증가 중 — 노출 우선순위 상향을 권장합니다</div>
        <div class="insight-row"><span class="insight-arrow">→</span>오늘 <strong>재료·알레르기 문의 11건</strong>이 AI에 의해 자동 처리됐습니다 (직원 응대 절감 약 22분)</div>
        <div class="insight-row"><span class="insight-arrow">→</span><strong>쏠불고기 태지갈비</strong>가 최근 3일간 리뷰 평점 하락 중 — 품질 점검을 권장합니다</div>
    </div>
    """, unsafe_allow_html=True)

    # 메뉴 순위 + 우측 패널
    col_left, col_right = st.columns([1.4, 1])

    with col_left:
        st.markdown('<div class="panel-title">메뉴 인기 순위</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-sub">오늘 주문 기준 · AI 노출 순서 자동 반영</div>', unsafe_allow_html=True)

        menus = [
            ("1위", "🍜", "하노이 분짜",      "₩13,000", 24, ["현지의 맛", "또 먹고 싶은"], "cyan"),
            ("2위", "🍲", "곱창 폭탄 쌀국수", "₩15,000", 18, ["곱창 양이 미쳤음", "이건 무조건"], "purple"),
            ("3위", "🥩", "쏠불고기 태지갈비","₩19,000", 11, [], ""),
            ("4위", "🍖", "파스타 리조또",    "₩14,000",  7, [], ""),
            ("5위", "🍕", "피자",             "₩16,000",  3, [], ""),
        ]
        max_orders = 24
        for rank, emoji, name, price, orders, tags, tag_color in menus:
            tag_html = "".join([f'<span class="tag-{tag_color}">{t}</span>' for t in tags])
            pct = int(orders / max_orders * 100)
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; padding:10px 0; border-bottom:1px solid #e8eaed;">
                <div style="font-size:11px; color:{'#00bcd4' if int(rank[0])<=2 else '#c4c7d4'}; width:24px; font-weight:700;">{rank}</div>
                <div style="font-size:20px;">{emoji}</div>
                <div style="flex:1;">
                    <div style="font-size:13px; font-weight:600;">{name}</div>
                    <div style="font-size:11px; color:#8b8fa8;">{price}</div>
                    {tag_html}
                </div>
                <div style="width:80px;">
                    <div style="height:4px; background:#f0f0f0; border-radius:99px; overflow:hidden;">
                        <div style="height:100%; width:{pct}%; background:#00bcd4; border-radius:99px;"></div>
                    </div>
                </div>
                <div style="font-size:12px; color:#8b8fa8; width:24px; text-align:right;">{orders}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        # 품절 관리
        st.markdown('<div class="panel-title">품절 관리</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-sub">변경 즉시 오더 화면에 반영</div>', unsafe_allow_html=True)

        if "soldout_1" not in st.session_state:
            st.session_state.soldout_1 = False
        if "soldout_2" not in st.session_state:
            st.session_state.soldout_2 = False

        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.markdown("<div style='font-size:13px; font-weight:600;'>돼지국밥</div><div style='font-size:11px; color:#8b8fa8;'>재고 소진 · 15분 전</div>", unsafe_allow_html=True)
        with col_b:
            st.toggle("판매가능", key="soldout_1")

        st.markdown("<hr>", unsafe_allow_html=True)

        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.markdown("<div style='font-size:13px; font-weight:600;'>곱창 폭탄 쌀국수</div><div style='font-size:11px; color:#8b8fa8;'>재고 부족 · AI 감지</div>", unsafe_allow_html=True)
        with col_b:
            st.toggle("판매가능", key="soldout_2")

        st.markdown("<br>", unsafe_allow_html=True)

        # 시간대별 주문 차트
        st.markdown('<div class="panel-title">시간대별 주문</div>', unsafe_allow_html=True)
        chart_data = pd.DataFrame({
            "주문수": [8, 19, 23, 13, 5, 5, 15]
        }, index=["11시", "12시", "13시", "14시", "15시", "16시", "17시"])
        st.bar_chart(chart_data, color="#00bcd4", height=160)

    st.markdown("<br>", unsafe_allow_html=True)

    # AI 문의 응답 로그
    st.markdown('<div class="panel-title">AI 자동 문의 응답 로그</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-sub">오늘 18건 자동 처리 — 직원 개입 0건</div>', unsafe_allow_html=True)

    inquiries = [
        ("🙋 \"이 메뉴에 땅콩 들어가나요? 알레르기가 있어서요\"",
         "하노이 분짜에는 땅콩이 포함되지 않습니다. 주요 알레르기 성분: 밀, 대두. 곱창 폭탄 쌀국수도 땅콩 미포함이나 조리 환경상 혼입 가능성이 있으니 주의 부탁드립니다."),
        ("🙋 \"이 집에서 제일 잘 팔리는 메뉴가 뭐예요?\"",
         "오늘 가장 많이 주문된 메뉴는 하노이 분짜(24건)입니다. 리뷰 4.8점으로 \"현지의 맛\", \"곱창 양이 미쳤음\" 키워드가 많습니다."),
        ("🙋 \"주차 가능한가요?\"",
         "건물 지하 주차장 이용 가능합니다. 2시간 무료, 이후 10분당 500원입니다."),
    ]
    for q, a in inquiries:
        st.markdown(f"""
        <div class="inquiry-q">{q}</div>
        <div class="inquiry-a"><span class="ai-badge">AI</span>{a}</div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════
# 메뉴 관리
# ════════════════════════════════════════════
elif page == "◎  메뉴 관리":

    st.markdown('<div class="page-title">메뉴 관리</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">전체 메뉴 · 노출 순서 · 품절 상태를 한 곳에서 관리하세요</div>', unsafe_allow_html=True)

    if "menu_data" not in st.session_state:
        st.session_state.menu_data = pd.DataFrame([
            {"메뉴명": "하노이 분짜",      "가격": 13000, "오늘 주문": 24, "리뷰 평점": 4.8, "노출 순위": 1, "판매 중": True},
            {"메뉴명": "곱창 폭탄 쌀국수", "가격": 15000, "오늘 주문": 18, "리뷰 평점": 4.6, "노출 순위": 2, "판매 중": True},
            {"메뉴명": "쏠불고기 태지갈비","가격": 19000, "오늘 주문": 11, "리뷰 평점": 4.2, "노출 순위": 3, "판매 중": True},
            {"메뉴명": "파스타 리조또",    "가격": 14000, "오늘 주문":  7, "리뷰 평점": 4.5, "노출 순위": 4, "판매 중": True},
            {"메뉴명": "피자",             "가격": 16000, "오늘 주문":  3, "리뷰 평점": 4.1, "노출 순위": 5, "판매 중": True},
            {"메뉴명": "돼지국밥",         "가격": 10000, "오늘 주문":  0, "리뷰 평점": 4.3, "노출 순위": 6, "판매 중": False},
        ])

    edited = st.data_editor(
        st.session_state.menu_data,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "가격": st.column_config.NumberColumn("가격 (원)", format="₩%d"),
            "리뷰 평점": st.column_config.NumberColumn("리뷰 평점", format="★ %.1f"),
            "판매 중": st.column_config.CheckboxColumn("판매 중"),
            "노출 순위": st.column_config.NumberColumn("노출 순위"),
        },
        hide_index=True,
    )

    if st.button("변경사항 저장", type="primary"):
        st.session_state.menu_data = edited
        st.success("저장됐어요! 오더 화면에 즉시 반영됩니다.")


# ════════════════════════════════════════════
# AI 추천 설정
# ════════════════════════════════════════════
elif page == "✦  AI 추천 설정":

    st.markdown('<div class="page-title">AI 추천 설정</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">AI가 메뉴를 추천하는 방식과 기준을 설정하세요</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="panel-title">노출 우선순위 가중치</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-sub">AI가 메뉴 상단 노출 순서를 결정할 때 사용하는 기준</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        w1 = st.slider("주문 빈도", 0, 100, 40, help="최근 7일 주문 수 기반")
        w2 = st.slider("리뷰 평점", 0, 100, 35, help="누적 리뷰 평균 점수")
        w3 = st.slider("수익성",   0, 100, 25, help="판매가 대비 마진율")
        total = w1 + w2 + w3

        if total != 100:
            st.warning(f"가중치 합계: {total}% — 100%가 되도록 조정해주세요")
        else:
            st.success("가중치 합계: 100% ✓")

        if st.button("설정 저장", type="primary"):
            st.success("저장됐어요! AI 추천 기준이 업데이트됩니다.")

    with col2:
        st.markdown('<div class="panel-title">AI 자동 응답 범위</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-sub">손님 문의 중 AI가 자동으로 답변할 항목</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        r1 = st.toggle("재료 · 알레르기 문의",        value=True,  help="메뉴 DB 기반 자동 응답")
        r2 = st.toggle("인기 메뉴 · 추천 문의",        value=True,  help="주문 데이터 기반 답변")
        r3 = st.toggle("가게 정보 문의 (주차, 영업시간)", value=True, help="등록된 가게 정보로 자동 답변")
        r4 = st.toggle("불만 · 민감 문의",             value=False, help="직원에게 직접 연결 (AI 미처리)")

        auto_rate = sum([r1, r2, r3]) * 29
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="insight-box">
            <div class="insight-title">✦ 예측 자동화율</div>
            <div class="insight-row"><span class="insight-arrow">→</span>현재 설정 기준 일평균 문의 자동 처리 <strong>약 {auto_rate}%</strong> 예상</div>
            <div class="insight-row"><span class="insight-arrow">→</span>직원 응대 절감 약 <strong>{auto_rate // 10 * 3}분/일</strong></div>
        </div>
        """, unsafe_allow_html=True)
