import streamlit as st
import time

# --- 페이지 설정 ---
st.set_page_config(
    page_title="Med-Study OS Demo",
    page_icon="🩺",
    layout="wide"
)

# --- CSS 스타일링 (예쁘게 꾸미기) ---
st.markdown("""
<style>
    .big-font { font-size:20px !important; font-weight: bold; }
    .highlight { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# --- 세션 상태 초기화 (단계별 진행을 위해) ---
if 'step' not in st.session_state:
    st.session_state.step = 0  # 0: 대기, 1: 분석중, 2: 알림발생, 3: 매칭결과, 4: 스크랩완료

# ==========================================
# [Header] 상단 제목
# ==========================================
st.title("🩺 Med-Study OS: 실시간 강의 연동 데모")
st.markdown("##### :mute: 강의를 듣는 동안 AI가 기출문제를 실시간으로 찾아줍니다.")
st.divider()

# ==========================================
# [Main] 화면 구성 (좌: 강의록 / 우: AI 패널)
# ==========================================
col1, col2 = st.columns([1.5, 1])

# --- 왼쪽: 강의록 뷰어 (이미지 교체 방식) ---
with col1:
    st.subheader("📄 강의록 뷰어 (PDF)")
    
    if st.session_state.step < 3:
        # 1. 기본 강의록 표지
        try:
            st.image("img_lecture_cover.png", caption="현재 보고 있는 페이지", use_container_width=True)
        except:
            st.warning("이미지 파일(img_lecture_cover.png)을 같은 폴더에 넣어주세요.")
            
    elif st.session_state.step == 3:
        # 2. 족보 매칭된 페이지 (자동 이동)
        st.image("img_lecture_match.png", caption="✅ AI가 찾아낸 연관 페이지 (14p. 뇌신경)", use_container_width=True)
        
    elif st.session_state.step == 4:
        # 3. 스크랩 완료된 페이지
        st.image("img_lecture_scrap.png", caption="✨ 내 노트에 저장 완료!", use_container_width=True)

# --- 오른쪽: AI 기능 패널 ---
with col2:
    st.subheader("🤖 AI 학습 비서")
    
    # [Step 0] 시작 전
    if st.session_state.step == 0:
        st.info("강의 녹음을 시작하면 실시간 분석이 진행됩니다.")
        if st.button("🔴 실시간 분석 시작 (Start)", type="primary"):
            st.session_state.step = 1
            st.rerun()

    # [Step 1~2] 분석 시뮬레이션 (Fake Loading)
    elif st.session_state.step == 1:
        status_text = st.empty()
        progress_bar = st.progress(0)
        
        # 3초 동안 듣는 척 연기하기
        for i in range(101):
            time.sleep(0.03) 
            progress_bar.progress(i)
            if i < 50:
                status_text.markdown("🎙️ **강의 듣는 중...** (STT 변환)")
            else:
                status_text.markdown("🔍 **핵심 키워드 감지:** 'Vagus Nerve'...")
        
        # 알림 발생
        st.toast("🚨 [족보 감지] 방금 교수님 말씀, 23년도 기출문제와 일치합니다!", icon="🔥")
        time.sleep(1)
        st.session_state.step = 3
        st.rerun()

    # [Step 3] 결과 확인 및 스크랩
    elif st.session_state.step >= 3:
        # 가짜 AI 분석 결과 표시
        with st.container(border=True):
            st.markdown("#### 🔥 기출 매칭 알림")
            st.markdown("**감지된 키워드:** 미주신경 (Vagus Nerve)")
            st.error("2023 중간고사 기출 (정답률 40%)")
            st.markdown("Q. 부교감 신경의 75%를 담당하는 뇌신경은?")
            st.caption("A. 10번 뇌신경 (CN X)")
            
            if st.session_state.step == 3:
                if st.button("📌 이 내용 강의록에 붙이기 (Scrap)"):
                    st.session_state.step = 4
                    st.toast("✅ 강의록 14페이지에 저장되었습니다!")
                    st.rerun()
            else:
                st.success("저장이 완료되었습니다.")
                if st.button("🔄 처음부터 다시 체험하기"):
                    st.session_state.step = 0
                    st.rerun()

# ==========================================
# [Survey] 설문조사 섹션 (데모 체험 후 하단 노출)
# ==========================================
st.divider()
st.header("📝 1분 설문조사")
st.markdown("방금 체험하신 기능이 실제로 구현된다면 어떨까요? 솔직한 의견을 들려주세요.")

with st.form("user_feedback"):
    # 질문 1: 가치 검증
    q1 = st.slider("Q1. '실시간 족보 매칭' 기능이 있다면, 시험 공부 시간이 얼마나 줄어들 것 같나요?", 
                   min_value=0, max_value=5, format="%d시간 이상")
    
    # 질문 2: WTP (지불 용의)
    q2 = st.radio("Q2. 이 기능이 포함된 'Med-Study OS'를 월 5,900원에 이용하실 의향이 있나요?", 
                  ("무조건 이용한다", "긍정적으로 고민해보겠다", "잘 모르겠다", "필요 없다"))
    
    # 질문 3: 주관식
    q3 = st.text_area("Q3. 현재 공부하면서 '자료 찾기' 때문에 가장 불편했던 점은 무엇인가요?")
    
    # 연락처 (선택)
    email = st.text_input("🎁 출시 알림 및 커피 쿠폰 추첨을 위한 이메일 (선택사항)")
    
    # 제출 버튼
    submitted = st.form_submit_button("의견 보내기 & 쿠폰 응모")
    
    if submitted:
        # 실제 데이터 저장 로직은 여기에 추가 (지금은 화면 표시만)
        st.balloons()
        st.success("소중한 의견 감사합니다! 여러분의 의견을 반영해 더 좋은 서비스를 만들겠습니다.")
        st.write(f"DEBUG(저장될 데이터): {q1}, {q2}, {q3}, {email}")