import streamlit as st
import pandas as pd
import json
import re
import io
from openai import OpenAI

st.set_page_config(page_title="번역 평가 검수 자동화", page_icon="🔍", layout="wide")

st.title("🔍 번역 평가 검수 자동화")
st.markdown("Gemini가 판정한 번역 오류 결과에서 **허위 오류를 자동으로 탐지**합니다.")

# ─── API 키 ───
with st.sidebar:
    st.header("⚙️ 설정")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    st.markdown("---")
    st.markdown("**검수 로직**")
    st.markdown("- **유형1** (코드): `marked_text`가 번역문에 없으면 → 허위 오류")
    st.markdown("- **유형2** (LLM): 번역문에 있지만 문법 지적이 틀리면 → 허위 오류")

# ─── 파일 업로드 ───
uploaded_file = st.file_uploader("📂 xlsx 파일 업로드", type=["xlsx"])

if not uploaded_file:
    st.info("위에서 번역 평가 결과 xlsx 파일을 업로드해주세요.")
    st.stop()

# ─── 데이터 로드 ───
@st.cache_data
def load_data(file):
    df = pd.read_excel(file, header=[0, 1, 2])
    df.columns = [' '.join([str(c) for c in col if 'Unnamed' not in str(c)]).strip() for col in df.columns]
    return df

try:
    raw_df = pd.read_excel(uploaded_file)
    df_raw = pd.read_excel(uploaded_file, header=None)
    
    header_row = None
    for i, row in df_raw.iterrows():
        if any('Segment ID' in str(v) for v in row.values):
            header_row = i
            break
    
    if header_row is None:
        header_row = 0
    
    df = pd.read_excel(uploaded_file, header=header_row)
    df.columns = [str(c).strip() for c in df.columns]
    
    seg_col = next((c for c in df.columns if 'Segment' in c or 'segment' in c.lower()), None)
    src_col = next((c for c in df.columns if 'Source' in c or 'KO' in c), None)
    trans_col = next((c for c in df.columns if 'Translation' in c or 'EN' in c), None)
    gemini_col = next((c for c in df.columns if 'Evaluation' in c or 'LLM' in c or 'MQM' in c), None)
    type_col = next((c for c in df.columns if '유형' in c or 'type' in c.lower()), None)

except Exception as e:
    st.error(f"파일 읽기 오류: {e}")
    st.stop()

if not all([seg_col, src_col, trans_col, gemini_col]):
    st.error("필요한 컬럼을 찾을 수 없습니다. 파일 구조를 확인해주세요.")
    with st.expander("감지된 컬럼 목록"):
        st.write(list(df.columns))
    st.stop()

df = df.dropna(subset=[seg_col, trans_col, gemini_col])
st.success(f"✅ {len(df)}개 세그먼트 로드 완료")

with st.expander("📋 원본 데이터 미리보기"):
    st.dataframe(df[[seg_col, src_col, trans_col]].head(5))

# ─── JSON 파싱 함수 ───
def parse_gemini_json(raw):
    try:
        raw = str(raw)
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    return None

# ─── 유형1: 코드 기반 검수 ───
def check_type1(marked_text, translation):
    if not marked_text or not translation:
        return None
    marked = str(marked_text).strip()
    if marked.lower() in str(translation).lower():
        return "O"
    else:
        return "X"

# ─── 유형2: LLM 기반 검수 ───
def check_type2(client, source, translation, marked_text, note):
    try:
        prompt = f"""You are a fact-checker. Answer only Y or N.

Is the expression "{marked_text}" grammatically and contextually correct in the following translation?

- Y: The expression is correct as is
- N: The expression contains a real grammatical or contextual error

Answer with only "Y" or "N". No explanation.

Source (KO): {source}
Translation (EN): {translation}
marked_text: {marked_text}
Gemini note: {note}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5,
            temperature=0
        )
        answer = response.choices[0].message.content.strip().upper()
        if "N" in answer:
            return "X"
        else:
            return "O"
    except Exception as e:
        return f"오류: {e}"

# ─── 검수 실행 ───
if st.button("🚀 검수 시작", type="primary"):
    if not api_key:
        st.error("OpenAI API Key를 입력해주세요.")
        st.stop()

    client = OpenAI(api_key=api_key)
    results = []

    progress = st.progress(0)
    status = st.empty()

    for idx, row in df.iterrows():
        seg_id = row[seg_col]
        source = row[src_col]
        translation = row[trans_col]
        gemini_raw = row[gemini_col]

        parsed = parse_gemini_json(gemini_raw)
        if not parsed or 'errors' not in parsed:
            results.append({
                "Segment ID": seg_id,
                "오류 번호": "-",
                "marked_text": "-",
                "note": "-",
                "유형": "-",
                "판정": "파싱 실패",
                "비고": "JSON 파싱 불가"
            })
            continue

        errors = parsed.get('errors', [])
        for err_idx, err in enumerate(errors):
            marked = err.get('marked_text', '')
            note = err.get('note', '')
            category = err.get('category', '')
            subtype = err.get('subtype', '')

            type1_result = check_type1(marked, translation)

            if type1_result == "X":
                verdict = "X (허위오류)"
                check_type = "유형1 (코드)"
                비고 = "번역문에 marked_text 없음"
            else:
                status.text(f"🔄 Segment {seg_id} - 오류 {err_idx+1} LLM 검수 중...")
                type2_result = check_type2(client, source, translation, marked, note)
                if type2_result == "O":
                    verdict = "X (허위오류)"
                    check_type = "유형2 (LLM)"
                    비고 = "문법 지적 부적절"
                else:
                    verdict = "O (유효)"
                    check_type = "유형2 (LLM)"
                    비고 = "실제 오류로 확인"

            results.append({
                "Segment ID": seg_id,
                "오류 번호": err_idx + 1,
                "category": category,
                "subtype": subtype,
                "marked_text": marked,
                "note": note,
                "검수 방식": check_type,
                "판정": verdict,
                "비고": 비고
            })

        progress.progress((list(df.index).index(idx) + 1) / len(df))

    status.empty()
    progress.empty()

    result_df = pd.DataFrame(results)
    st.session_state['result_df'] = result_df

# ─── 결과 표시 ───
if 'result_df' in st.session_state:
    result_df = st.session_state['result_df']

    st.markdown("---")
    st.subheader("📊 검수 결과")

    total = len(result_df[result_df['판정'] != '파싱 실패'])
    false_errors = len(result_df[result_df['판정'] == 'X (허위오류)'])
    valid = len(result_df[result_df['판정'] == 'O (유효)'])

    col1, col2, col3 = st.columns(3)
    col1.metric("전체 오류 항목", total)
    col2.metric("✅ 유효 오류", valid)
    col3.metric("❌ 허위 오류 탐지", false_errors, delta=f"{false_errors/total*100:.1f}%" if total > 0 else "0%")

    # ── applymap → map 으로 수정 ──
    def highlight_verdict(val):
        if val == 'X (허위오류)':
            return 'background-color: #ffcccc'
        elif val == 'O (유효)':
            return 'background-color: #ccffcc'
        return ''

    styled = result_df.style.map(highlight_verdict, subset=['판정'])
    st.dataframe(styled, use_container_width=True)

    if false_errors > 0:
        with st.expander(f"❌ 허위 오류 목록만 보기 ({false_errors}건)"):
            st.dataframe(result_df[result_df['판정'] == 'X (허위오류)'], use_container_width=True)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        result_df.to_excel(writer, index=False, sheet_name='검수결과')
    buffer.seek(0)

    st.download_button(
        label="📥 결과 다운로드 (xlsx)",
        data=buffer,
        file_name="번역_검수_결과.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
