import streamlit as st
import time
import os
import random

# --- 경로 설정 ---
current_dir = os.path.dirname(os.path.abspath(__file__))
# (이미지 파일명은 기존과 동일하다고 가정하거나, 더 리얼한 것으로 교체하세요)
img_cover_path = os.path.join(current_dir, "img_lecture_cover.png")
img_match_path = os.path.join(current_dir, "img_lecture_match.png")
img_scrap_path = os.path.join(current_dir, "img_lecture_scrap.png")

# --- 페이지 설정 (와이드 모드) ---
st.set_page_config(layout="wide", page_title="Med-Study OS Pro", page_icon="🧠")

# --- 세션 상태 초기화 ---
if 'step' not in st.session_state: st.session_state.step = 0
if 'notes' not in st.session_state: st.session_state.notes = ""
if 'accuracy' not in st.session_state: st.session_state.accuracy = 82

# --- 사이드바: 가짜 개인화 설정 ---
with st.sidebar:
    st.header("👤 내 프로필")
    st.info("박규민 (본과 1학년)님 환영합니다.")
    
    st.markdown("---")
    st.markdown("**🎓 학습 설정**")
    st.selectbox("목표 대학", ["경상국립대 의과대학", "서울대 의과대학", "연세대 의과대학"])
    st.selectbox("현재 과목", ["해부학 (Anatomy)", "약리학", "병리학"])
    
    st.markdown("---")
    st.markdown("**🧠 AI 엔진 상태**")
    # 가짜 그래프: 내가 쓸수록 똑똑해지는 느낌 주기
    st.caption(f"개인화 매칭 정확도: **{st.session_state.accuracy}%**")
    st.progress(st.session_state.accuracy / 100)
    if st.session_state.step >= 4:
        st.success("✨ 방금 데이터로 모델이 미세조정(Fine-tuned) 되었습니다.")

# --- 메인 화면: 탭 구성 ---
tab1, tab2 = st.tabs(["🖥️ 학습 스튜디오 (Study OS)", "📊 학습 분석 대시보드"])

with tab1:
    # 3단 분할 레이아웃 (강의록 | AI 비서 | 내 노트)
    col_pdf, col_ai, col_note = st.columns([2, 1.5, 1.2])

    # 1. 좌측: 강의록 뷰어
    with col_pdf:
        st.subheader("📄 Lecture View")
        def show_image(path):
            if os.path.exists(path):
                st.image(path, use_container_width=True)
            else:
                st.error("이미지 파일을 넣어주세요.")

        if st.session_state.step < 3:
            show_image(img_cover_path)
        elif st.session_state.step == 3:
            show_image(img_match_path)
            st.caption("✅ RAG Engine: 'Vagus Nerve' 관련 페이지 자동 이동됨")
        elif st.session_state.step == 4:
            show_image(img_scrap_path)

    # 2. 중앙: AI 챗봇 & 족보 알림
    with col_ai:
        st.subheader("🤖 AI Assistant")
        
        # 채팅창 UI 흉내
        with st.container(border=True, height=500):
            st.chat_message("ai").write("강의를 실시간으로 분석하고 있습니다... 🎧")
            
            if st.session_state.step >= 1:
                # 녹음 중 애니메이션 효과
                st.markdown("---")
                st.markdown("**:red[● Rec]** `00:14:23`")
                if st.session_state.step == 1:
                    with st.spinner("교수님 음성 텍스트 변환(STT) 및 족보 DB 검색 중..."):
                        time.sleep(3) # 3초 딜레이
                    st.session_state.step = 3
                    st.rerun()

            if st.session_state.step >= 3:
                time.sleep(0.5)
                st.chat_message("ai").markdown("""
                **🚨 [기출 매칭 감지]**
                
                방금 교수님이 강조하신 **'미주신경(Vagus Nerve)'** 내용은 **2023년도 1학기 중간고사**에 출제되었습니다.
                
                > **Q. 부교감 신경의 75%를 담당하는 뇌신경은?**
                > (정답률: 45% / 난이도: 상)
                
                관련 강의록 페이지를 펼쳤습니다.
                """)
                
                if st.session_state.step == 3:
                    if st.button("✨ 내 노트에 정리해서 넣기 (Auto-Scrap)", type="primary"):
                        # '학습'되는 척 연출
                        with st.status("📝 AI가 핵심 내용을 요약하고 노트에 적고 있습니다...", expanded=True) as status:
                            time.sleep(1)
                            st.write("🔍 관련 개념 추출 중...")
                            time.sleep(0.8)
                            st.write("✒️ 요약문 생성 중...")
                            time.sleep(0.8)
                            st.write("💾 Private Vault에 암호화 저장 중...")
                            status.update(label="스크랩 완료!", state="complete", expanded=False)
                        
                        st.session_state.notes += "\n\n[2023 기출] 미주신경(CN X)\n- 부교감신경의 75% 담당\n- 장기 대부분에 분포함\n(출처: 강의록 14p)"
                        st.session_state.accuracy += 5 # 정확도 상승 연출
                        st.session_state.step = 4
                        st.rerun()

    # 3. 우측: 나만의 스마트 노트
    with col_note:
        st.subheader("📒 My Smart Note")
        st.text_area("오늘의 필기", value=st.session_state.notes, height=500, placeholder="AI가 정리한 내용이 이곳에 자동으로 쌓입니다.")

    # 시작 버튼 (초기 상태일 때만 보임)
    if st.session_state.step == 0:
        st.info("⬇️ 아래 버튼을 눌러 강의 모니터링을 시작하세요.")
        if st.button("🚀 실시간 강의 분석 시작"):
            st.session_state.step = 1
            st.rerun()

# --- 설문조사 탭 (사업계획서 검증용) ---
with tab2:
    st.title("📋 베타테스터 피드백")
    st.markdown("Med-Study OS의 사업화를 위해 귀하의 솔직한 의견이 필요합니다.")
    
    with st.form("biz_survey"):
        st.subheader("1. 문제 인식 (Pain Point)")
        st.markdown("사업계획서 분석에 따르면 의대생은 하루 평균 **2시간**을 단순 검색에 쓴다고 합니다.")
        q1 = st.radio("실제 본인의 '자료 찾기/매칭' 스트레스는 어느 정도인가요?", 
                     ["극심함 (학습 흐름이 매번 끊김)", "보통 (귀찮지만 할 만함)", "전혀 없음"])
        
        st.subheader("2. 솔루션 검증 (Solution)")
        st.markdown("방금 보신 **'실시간 족보 매칭 & 자동 스크랩'** 기능이 구현된다면?")
        q2 = st.slider("시험 기간 하루 공부 시간이 얼마나 단축될 것 같나요?", 0, 4, 1, format="%d시간")
        
        st.subheader("3. 가격 정책 (Business Model)")
        st.markdown("커피 한 잔 값(월 5,900원)으로 이 모든 기능(무제한 스크랩, 족보 연동)을 쓴다면?")
        q3 = st.radio("구독 의향", ["무조건 구독 (사전 예약)", "긍정적 검토", "무료 버전에만 관심", "안 함"])
        
        st.subheader("4. 추가 기능 제안")
        q4 = st.text_area("이 기능 외에 '이것만 있으면 무조건 결제한다' 싶은 기능이 있나요?")
        
        contact = st.text_input("휴대전화/이메일 (베타 오픈 시 알림 및 1개월 무료 쿠폰 지급)")
        
        if st.form_submit_button("제출 및 쿠폰 받기"):
            st.balloons()
            st.success("소중한 의견이 개발팀(박규민 외)에 전달되었습니다. 감사합니다!")

