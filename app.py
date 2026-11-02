import streamlit as st
import anthropic

st.set_page_config(page_title="자기소개서 생성기", page_icon="✍️")
st.title("✍️ 자기소개서 생성기")

company = st.text_input("지원 회사")
job = st.text_input("지원 직무")
question = st.selectbox("문항", ["지원 동기", "직무 역량", "성장 과정", "입사 후 포부", "직접 입력"])
if question == "직접 입력":
    question = st.text_input("문항 내용을 입력하세요")
experience = st.text_area("핵심 경험·강점 (메모 형태도 괜찮습니다)", height=200)
length = st.slider("분량 (글자 수)", 300, 1500, 700, 100)
tone = st.radio("문체", ["격식체", "담백한 문체"], horizontal=True)

if st.button("자소서 생성"):
    if not (company and job and experience):
        st.warning("회사, 직무, 경험을 모두 입력해 주세요.")
    else:
        prompt = f"""다음 정보로 자기소개서 한 문항을 작성해 주세요.
- 지원 회사: {company}
- 지원 직무: {job}
- 문항: {question}
- 분량: 약 {length}자
- 문체: {tone}
- 지원자의 경험·강점: {experience}

규칙: 위에 적힌 경험만 사용하고, 없는 사실이나 수치는 지어내지 마세요."""
        client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
        with st.spinner("작성 중입니다..."):
            msg = client.messages.create(
                model="claude-sonnet-5-5",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )
        st.subheader("초안")
        st.write(msg.content[0].text)