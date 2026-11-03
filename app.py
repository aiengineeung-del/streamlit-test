import os
import streamlit as st
from openai import OpenAI

openai_key = st.secrets["OPENAI_API_KEY"]
MODEL = "gpt-4o-mini"  # 사용 가능한 모델명으로 바꾸실 수 있습니다

def get_api_key():
    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="자기소개서 생성기", page_icon="✍️")
st.title("✍️ 자기소개서 생성기")

with st.form("cover_letter_form"):
    company = st.text_input("지원 회사")
    job = st.text_input("지원 직무")
    question = st.selectbox("문항", ["지원 동기", "직무 역량", "성장 과정", "입사 후 포부"])
    custom_q = st.text_input("직접 입력 문항 (선택, 입력하면 위 문항 대신 사용)")
    experience = st.text_area("핵심 경험·강점 (메모 형태도 괜찮습니다)", height=200)
    length = st.slider("분량 (글자 수)", 300, 1500, 700, 100)
    tone = st.radio("문체", ["격식체", "담백한 문체"], horizontal=True)
    submitted = st.form_submit_button("자소서 생성")

if custom_q:
    question = custom_q

if submitted:
    if not (company and job and experience):
        st.warning("회사, 직무, 경험을 모두 입력해 주세요.")
    elif "OPENAI_API_KEY" not in st.secrets:
        st.error("API 키가 등록되지 않았습니다. 앱 Settings → Secrets를 확인해 주세요.")
    else:
        # 이 아래는 기존 prompt = ... 부터 st.write(...) 까지 그대로
        prompt = f"""다음 정보로 자기소개서 한 문항을 작성해 주세요.
- 지원 회사: {company}
- 지원 직무: {job}
- 문항: {question}
- 분량: 약 {length}자
- 문체: {tone}
- 지원자의 경험·강점: {experience}

규칙: 위에 적힌 경험만 사용하고, 없는 사실이나 수치는 지어내지 마세요."""
try:
    client = OpenAI(api_key=openai_key)
    with st.spinner("작성 중입니다..."):
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
    st.subheader("초안")
    st.write(resp.choices[0].message.content)
except Exception as e:
    st.error(f"요청 중 오류가 발생했습니다: {type(e).__name__}")