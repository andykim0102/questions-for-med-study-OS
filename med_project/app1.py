import streamlit as st
import time
import os

# --- 설정 및 경로 ---
st.set_page_config(layout="wide", page_title="Med-Study OS Pro", page_icon="🩺")
current_dir = os.path.dirname(os.path.abspath(__file__))

# 이미지 경로 (자동 탐지)
img_paths = {
    "cover": os.path.join(current_dir, "img_dashboard.png"),
    "match": os.path.join(current_dir, "img_match.png"),
    "scrap": os.path.join(current_dir, "img_scrap.png")
}

# --- CSS 스타일링 (SaaS 느낌 내기) ---
st.markdown("""
<style>
    /* 전체 배경 및 폰트 */
    .stApp { background-color: #f8f9fa; }
    h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; }
    
    /* 카드 스타일 */
    .metric-card {
        background-color: white; border: 1px solid #e0e0e0; 
        padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        text-align: center;
    }
    
    /* AI 채팅창 스타일 */
    .ai-bubble {
        background-color: #e3f2fd; padding: 15px; border-radius: 15px;
        margin-bottom: 10px; border-left: 5px solid #2196f3;
    }
    
    /* 버튼 커스텀 */
    .stButton>button {
        width: 100%; border-radius: 8px; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- 세션 상태 초기화 ---
if 'state' not in st.session_state: st.session_state.state = 'dashboard'
if 'scrap_count' not in st.session_state: st.session_state.scrap_count = 12
if 'saved_time' not in st.session_state: st.session_state.saved_time = 45

# ==========================================
# [Header] 상단 네비게이션 바 흉내
# ==========================================
col_logo, col_menu, col_user = st.columns([1, 3, 1])
with col_logo:
    st.markdown("### 🩺 Med-Study OS")
with col_menu:
    st.caption("Ver 1.0.2 Beta | Connected to: SNU_Med_Anatomy_DB")
with col_user:
    st.markdown("**박규민 (본과 1학년)** 님")

st.divider()

# ==========================================
# [Scene 1] 메인 대시보드 (학습 현황)
# ==========================================
if st.session_state.state == 'dashboard':
    st.subheader("📊 My Learning Dashboard")
    
    # 지표 카드 (사업계획서의 '시간 단축' 가치 강조)
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='metric-card'><h3>오늘 절약한 시간</h3><h2 style='color:#2196f3'>{st.session_state.saved_time}분</h2></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'><h3>정리한 족보</h3><h2>{st.session_state.scrap_count}개</h2></div>", unsafe_allow_html=True)
    c3.markdown("<div class='metric-card'><h3>매칭 정확도</h3><h2>92%</h2></div>", unsafe_allow_html=True)
    c4.markdown("<div class='metric-card'><h3>시험 D-Day</h3><h2 style='color:#ff5252'>D-14</h2></div>", unsafe_allow_html=True)

    st.markdown("### 📚 최근 학습 강의")
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        if os.path.exists(img_paths["cover"]):
            st.image(img_paths["cover"], caption="[Anatomy] Cranial Nerves & ANS - Prof. Kim", use_container_width=True)
        else:
            st.error("이미지 파일(img_dashboard.png)이 없습니다.")
            
    with col_side:
        st.info("💡 **AI 알림:** 어제 학습 중 '미주신경(Vagus Nerve)' 관련 기출문제 분석이 완료되었습니다.")
        if st.button("🚀 학습 이어하기 (Enter Workspace)", type="primary"):
            st.session_state.state = 'workspace_init'
            st.rerun()

# ==========================================
# [Scene 2] 워크스페이스 (솔루션 핵심 기능)
# ==========================================
elif st.session_state.state.startswith('workspace'):
    # 3단 분할: PDF 뷰어 | 족보 리스트 | AI 인터랙션
    col_pdf, col_tool = st.columns([1.8, 1])
    
    # --- 좌측: PDF 뷰어 ---
    with col_pdf:
        st.markdown("#### 📄 Lecture Note Viewer")
        if st.session_state.state == 'workspace_init':
            st.image(img_paths["cover"], use_container_width=True)
        elif st.session_state.state == 'workspace_match':
            st.image(img_paths["match"], caption="✅ Smart Source Matching: 14p 자동 이동됨", use_container_width=True)
        elif st.session_state.state == 'workspace_done':
            st.image(img_paths["scrap"], caption="✨ Private Vault에 저장 완료", use_container_width=True)

    # --- 우측: 도구 모음 ---
    with col_tool:
        # 탭 구성
        tab1, tab2 = st.tabs(["🔥 족보(Past Exams)", "🤖 AI Tutor"])
        
        with tab1:
            st.markdown("**2023-1학기 중간고사 기출**")
            
            # 기출문제 리스트 (클릭 유도)
            with st.container(border=True):
                st.error("Q4. 부교감 신경의 75%를 담당하는 뇌신경은? (난이도: 상)")
                if st.button("🔍 출처 찾기 (Source Matching)"):
                    # 로딩 연출 (RAG 엔진 작동 흉내)
                    with st.spinner("RAG 엔진이 강의록 벡터 DB를 검색 중입니다..."):
                        time.sleep(1.5)
                    st.toast("매칭 성공! 관련 페이지(14p)를 펼쳤습니다.", icon="✅")
                    st.session_state.state = 'workspace_match'
                    st.rerun()
            
            st.caption("다른 문제들은 Pro 버전에서 확인 가능합니다.")

        with tab2:
            if st.session_state.state == 'workspace_match':
                st.markdown("<div class='ai-bubble'><b>🤖 Med-OS AI</b><br>해당 문제는 <b>'미주신경(CN X)'</b>의 분포 범위와 기능을 묻고 있습니다.<br><br>강의록 14페이지 하단 다이어그램에서 출제 근거를 찾았습니다.</div>", unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("**액션 선택:**")
                
                if st.button("📌 스마트 스크랩 (Drag & Drop Simulation)", type="primary"):
                    with st.status("📝 요약 노트 생성 중...", expanded=True):
                        st.write("텍스트 추출 중...")
                        time.sleep(0.5)
                        st.write("핵심 요약 생성 중...")
                        time.sleep(0.5)
                        st.write("강의록에 부착 중...")
                        time.sleep(0.5)
                    st.session_state.state = 'workspace_done'
                    st.session_state.scrap_count += 1
                    st.session_state.saved_time += 15
                    st.rerun()
            else:
                st.info("족보 문제를 선택하면 AI가 분석을 시작합니다.")

    # 설문조사로 넘어가는 버튼
    if st.session_state.state == 'workspace_done':
        st.divider()
        if st.button("✅ 체험 종료 및 의견 남기기 (Next Step)"):
            st.session_state.state = 'survey'
            st.rerun()

# ==========================================
# [Scene 3] 사업계획서 검증용 설문조사
# ==========================================
elif st.session_state.state == 'survey':
    st.markdown("## 📋 Product Market Fit(PMF) 검증")
    st.success(f"방금 기능을 통해 기존 10분 걸리던 작업을 **30초** 만에 끝냈습니다.")
    
    with st.form("validation_form"):
        # 1. Pain Point 검증 (사업계획서 P.2 배경)
        st.markdown("### 1. 문제 인식 (Problem)")
        st.caption("사업계획서 가설: 의대생은 단순 자료 대조에 일평균 2시간을 허비한다.")
        q1 = st.slider("Q. 평소 공부할 때 '자료 찾기/Alt-Tab'으로 인한 피로도는 몇 점인가요?", 1, 10, 8)
        
        # 2. Solution 검증 (사업계획서 P.3 실현가능성)
        st.markdown("### 2. 솔루션 가치 (Solution)")
        st.caption("방금 체험한 'Smart Source Matching'과 'Scraping' 기능입니다.")
        q2 = st.radio("Q. 이 기능을 사용하면 시험 기간 공부 시간이 얼마나 단축될 것 같나요?", 
                      ["변화 없음", "30분 미만", "1시간 정도", "2시간 이상 (획기적임)"])
        
        # 3. WTP 검증 (사업계획서 P.6 수익모델)
        st.markdown("### 3. 가격 정책 (Price)")
        st.caption("Med-Study OS Pro: 무제한 스크랩 + Private Vault 제공")
        q3 = st.selectbox("Q. 월 5,900원(커피 한 잔 값)에 구독하실 의향이 있나요?", 
                          ["반드시 구독함", "긍정적 검토", "기능이 더 추가되면 고려", "아니오"])
        
        # 4. 리드 수집
        email = st.text_input("🎁 출시 알림 및 베타테스터 신청 (이메일)")
        
        if st.form_submit_button("제출 및 결과 보기"):
            st.balloons()
            st.success("소중한 의견 감사합니다! 여러분의 피드백으로 더 완벽한 OS를 만들겠습니다.")
            st.write("---")
            st.markdown(f"**[Debug] 수집된 데이터:** 피로도({q1}), 시간단축({q2}), 구독의향({q3})")
            if st.button("🔄 다시 체험하기"):
                st.session_state.state = 'dashboard'
                st.rerun()
