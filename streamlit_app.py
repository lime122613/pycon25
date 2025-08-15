import streamlit as st
tab1, tab2, tab3 = st.tabs(["사진", "공유 시트 보기","공유 시트 쓰기"])  # 2개의 탭 생성
with tab1:
    st.title("😊 자모옹의 첫 번째 앱 💕")
    st.info("안녕하세요~! 파이콘 튜토리얼 예제 앱입니다!")

    st.subheader("사진첩")
    st.write(
        "내가 좋아하는 동물을 소개해봅시다!"
    )
    st.image("https://img.animalplanet.co.kr/news/2022/10/13/700/gzs211818b42g2a88a13.jpg", caption="행복한 쿼카", use_container_width=True)

    st.link_button("네이버 바로가기", 'https://naver.com')


with tab2:
    # import pandas as pd

    # st.title("1️⃣ ✅ 공개 Google Sheet 읽기")
    # st.info("📘 누구나 볼 수 있도록 공개된 시트를 Pandas로 직접 불러오는 가장 간단한 방법입니다.\n📎 링크는 반드시 `export?format=csv` 형태로 설정하세요.")

    # csv_url1 = "https://docs.google.com/spreadsheets/d/1VC_q8HJfIufjGVR2zGRcJjBgkefIbp6Pv01rQ1uvoXI/export?format=csv"
    # df1 = pd.read_csv(csv_url1)
    # st.dataframe(df1)
    # st.dataframe(df1['question_id','choice'])

    import pandas as pd

    st.title("2️⃣ 🔐 공개 Google Sheet 읽기")
    st.info("📘 Sheet는 여전히 공개 상태입니다. URL만 안전하게 숨기기 위해 `secrets.toml`에 저장합니다.")
    # st.write(st.secrets["pw"]["key"]) #pw그룹 안에 있는 key 변수 쓰기

    csv_url2 = st.secrets["gsheet_public_csv_url"] #url을 st.secrets로 불러옴.  secret 폴더를 만들어야함. 
    df2 = pd.read_csv(csv_url2)

    # 📄 시트 전체 미리보기
    st.dataframe(df2, use_container_width=True)

    # 🔍 활성화된 질문 필터링
    active_rows = df2[df2["is_active"] == True]

    if active_rows.empty:
        st.warning("⚠️ 현재 활성화된 질문이 없습니다.")
    else:
        for i, row in active_rows.iterrows():
            st.divider()
            st.subheader(f"📌 질문: {row['question_text']}")
            
            # 선택지 opt_a, opt_b, opt_c, ... 자동 추출
            options = [row[col] for col in df2.columns if col.startswith("opt_") and pd.notna(row[col])]
            
            # 사용자 응답 입력
            selected = st.radio(
                f"답을 골라주세요 (질문 ID: {row['question_id']})",
                options,
                key=f"question_{i}"
            )

            # ✅ 정답 확인
            correct = row["answer"]
            if selected:
                if selected == correct:
                    st.success("✅ 정답입니다!")
                else:
                    st.error(f"❌ 오답입니다. 정답은 **{correct}** 입니다.")

with tab3:
    import gspread
    import pandas as pd
    from google.oauth2.service_account import Credentials

    # 앱 제목 출력
    st.title("3️⃣ 🔒 비공개 Google Sheet 연결")

    # 서비스 계정 설정 안내
    st.info(
        "🔐 시트에 ‘공개 설정 없이’ 안전하게 접근하려면 서비스 계정을 사용해야 합니다.\n"
        "📎 서비스 계정 이메일을 시트에 ‘뷰어’ 또는 ‘편집자’로 공유하세요."
    )

    # Google API 접근 범위(SCOPES) 설정
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",  # 구글 스프레드시트 읽기/쓰기
        "https://www.googleapis.com/auth/drive"          # 구글 드라이브 접근
    ]

    # secrets.toml에 저장된 서비스 계정 정보로 인증 객체 생성
    credentials = Credentials.from_service_account_info(
        st.secrets["google_service_account"],  # 서비스 계정 JSON 데이터
        scopes=SCOPES
    )

    # gspread를 이용해 구글 시트 API 인증
    gc = gspread.authorize(credentials)

    # secrets.toml에 저장된 시트 키로 구글 시트 열기
    spreadsheet = gc.open_by_key(st.secrets["gsheet_key"])

    # "datainput" 워크시트 선택
    sheet_input = spreadsheet.worksheet("시트1")

    # 데이터 추가 함수 정의
    def append_input_data(name, feedback):
        """
        Google Sheet의 'datainput' 워크시트에 한 행(name, feedback) 추가
        """
        sheet_input.append_row([name, feedback])

    # 입력 폼 생성
    with st.form("input_form"):
        name = st.text_input("이름")            # 이름 입력
        feedback = st.text_area("피드백")       # 피드백 입력
        submitted = st.form_submit_button("제출")

        if submitted:
            # 이름과 피드백이 모두 입력된 경우
            if name and feedback:
                append_input_data(name, feedback)     # 시트에 데이터 저장
                st.success("✅ 저장 완료")             # 성공 메시지
            else:
                st.warning("⚠️ 모든 필드를 입력해 주세요.")  # 경고 메시지

    # 구분선
    st.markdown("---")
    st.subheader("📊 지금까지 제출된 데이터")

    # Google Sheet의 모든 데이터 읽어서 DataFrame 변환
    df = pd.DataFrame(sheet_input.get_all_records())

    # 새로고침 버튼 클릭 시 캐시 삭제 → 최신 데이터 반영
    if st.button("새로고침 🔄"):
        st.cache_data.clear()

    # 피드백 컬럼 데이터 화면에 표시
    st.write(df['피드백'])
