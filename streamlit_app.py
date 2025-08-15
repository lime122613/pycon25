import streamlit as st

st.title("🎈 😊자모옹의 파이콘 튜토리얼💕")
st.info("안녕하세요~! 파이콘 튜토리얼 예제 앱입니다!")

st.subheader("첫 번째 앱")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
st.image("https://img.animalplanet.co.kr/news/2022/10/13/700/gzs211818b42g2a88a13.jpg", caption="행복한 쿼카", use_container_width=True)

st.code("""
import streamlit as st
st.title('Hello World')
""", language="python")

st.write('https://naver.com')
st.link_button("네이버 바로가기", 'https://naver.com')

