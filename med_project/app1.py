import streamlit as st
import time
import random

# --- 페이지 설정 (브라우저 탭 이름 등) ---
st.set_page_config(
    page_title="Med-Study OS: Pro",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 세션 상태 초기화 ---
if 'step' not in st.session_state: st.session_state.step = 'dashboard'
if 'analysis_done' not in st.session_state: st.session_state.analysis_done = False
if 'notes' not in st.session_state: st.session_state.notes = ""

# --- 고급 스타일링 (CSS) ---
st.markdown("""
<style>
    /* 전체 폰트: 프리텐다드 적용 */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    * { font-family: 'Pretendard', sans-serif; }
    
    /* 메인 배경색 */
    .stApp { background-color: #f8f9fa; }
    
    /* 대시보드 카드 스타일 */
    .dashboard-card {
        background-color: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center;
        border: 1px solid #e9ecef; transition: transform 0.2s;
    }
    .dashboard-card:hover { transform: translateY(-5px); }
    
    /* 로그 창 스타일 (해킹/개발자 모드 느낌) */
    .terminal-box {
        background-color: #1e1e1e; color: #00ff00; padding: 15px;
        border-radius: 8px; font-family: 'Courier New', monospace; font-size: 13px;
        height: 150px; overflow-y: auto; border: 1px solid #333;
    }
    
    /* 스마트 노트 스타일 */
    .smart-note {
        background-color: #fff9c4; border-left: 6px solid #fbc02d;
        padding: 20px; border-radius: 4px; box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        font-family: 'Gaegu', cursive;
    }
    
    /* 하이라이트 효과 */
    .highlight-text { background-color: #fff176; padding: 2px 4px; border-radius: 3px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 사이드바: 사용자 프로필 (사업계획서 기반) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=80)
    st.markdown("### 👤 **박규민** (본과 1학년)")
    st.caption("경상국립대 의과대학 | Top 5%")
    st.divider()
    
    st.markdown("**⚙️ Med-Study OS Status**")
    st.markdown("- **Engine:** Ver 2.1.0 (Stable)")
    st.markdown("- **DB Connection:** Connected 🟢")
    st.markdown("- **Private Vault:** Secured 🔒")
    st.divider()
    
    if st.button("🔄 세션 초기화 (Reset)", use_container_width=True):
        st.session_state.step = 'dashboard'
        st.session_state.analysis_done = False
        st.rerun()

# ==========================================
# [Scene 1] 메인 대시보드 (압도적인 첫인상)
# ==========================================
if st.session_state.step == 'dashboard':
    st.title("Med-Study OS: Intelligent Workspace")
    st.markdown("##### 🚀 의대생의 학습 시간을 **120분에서 18분**으로 단축합니다.")
    
    # 핵심 지표 (KPI) - 사업계획서 수치 반영
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown("""<div class='dashboard-card'><h3>⏳ 절약한 시간</h3><h1 style='color:#2196f3'>45분</h1><p>오늘 하루 기준</p></div>""", unsafe_allow_html=True)
    col2.markdown("""<div class='dashboard-card'><h3>📚 단권화 완료</h3><h1 style='color:#4caf50'>12건</h1><p>Private Vault 저장됨</p></div>""", unsafe_allow_html=True)
    col3.markdown("""<div class='dashboard-card'><h3>🎯 매칭 정확도</h3><h1 style='color:#ff9800'>94%</h1><p>Ground Truth 기반</p></div>""", unsafe_allow_html=True)
    col4.markdown("""<div class='dashboard-card'><h3>🔥 시험 D-Day</h3><h1 style='color:#f44336'>D-14</h1><p>해부학(Anatomy)</p></div>""", unsafe_allow_html=True)

    st.markdown("---")
    
    # 자료 업로드 섹션 (사용자가 직접 시연)
    st.subheader("📂 New Study Session (자료 업로드)")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            st.info("📄 **Step 1. 강의록(Source)**을 업로드하세요.")
            lec_file = st.file_uploader("PDF 또는 이미지 파일", type=['png', 'jpg', 'pdf'], key='lec')
        with c2:
            st.warning("❓ **Step 2. 족보/기출(Problem)**을 업로드하세요.")
            exam_file = st.file_uploader("이미지 파일", type=['png', 'jpg'], key='exam')
            
        if lec_file and exam_file:
            st.session_state.lec_file = lec_file
            st.session_state.exam_file = exam_file
            st.success("✅ 자료 준비 완료! RAG 엔진을 가동합니다.")
            if st.button("🚀 AI 분석 및 단권화 시작 (Start)", type="primary", use_container_width=True):
                st.session_state.step = 'processing'
                st.rerun()

# ==========================================
# [Scene 2] AI 분석 시뮬레이션 (기술력 과시)
# ==========================================
elif st.session_state.step == 'processing':
    st.title("⚙️ Processing Data...")
    
    c_img, c_log = st.columns([1, 1.2])
    
    with c_img:
        st.image(st.session_state.lec_file, caption="Scanning Document...", width=400)
    
    with c_log:
        st.markdown("**📡 System Kernel Logs**")
        log_placeholder = st.empty()
        bar = st.progress(0)
        
        # 있어 보이는 로그 메시지들
        logs = [
            "[INIT] Initializing Med-Study OCR Engine...",
            "[READ] Extracting text layers from PDF source...",
            "[EMBED] Vectorizing content (Dimension: 1536)...",
            "[SEARCH] Querying 'Ground Truth' Database (1,000 sets)...",
            "[MATCH] Identifying Key Concepts: 'Vagus Nerve', 'CN X'...",
            "[LINK] Context-Link Established (Confidence: 99.2%)...",
            "[GEN] Generating Smart Summary for User...",
            "[DONE] Analysis Complete. Preparing Workspace."
        ]
        
        current_log = ""
        for i, log in enumerate(logs):
            time.sleep(random.uniform(0.4, 0.8)) # 랜덤 딜레이로 리얼함 더하기
            current_log += f"{log}\n"
            log_placeholder.markdown(f"<div class='terminal-box'>{current_log}</div>", unsafe_allow_html=True)
            bar.progress((i + 1) * 12)
            
        time.sleep(0.5)
        st.session_state.step = 'workspace'
        st.rerun()

# ==========================================
# [Scene 3] 결과 워크스페이스 (통합 뷰)
# ==========================================
elif st.session_state.step == 'workspace':
    st.header("🎓 Smart Study Workspace")
    
    # 3단 분할 레이아웃 (강의록 - AI비서 - 노트)
    col_main, col_sub = st.columns([1.8, 1.2])
    
    with col_main:
        st.subheader("📄 Lecture View (Auto-Navigated)")
        st.image(st.session_state.lec_file, use_container_width=True)
        st.caption("✅ AI가 기출문제와 연관된 페이지를 자동으로 찾았습니다.")

    with col_sub:
        # 탭으로 기능 분리
        tab1, tab2 = st.tabs(["🤖 AI Tutor & Match", "📒 My Smart Note"])
        
        with tab1:
            st.markdown("#### 🚨 기출 매칭 알림")
            with st.container(border=True):
                st.image(st.session_state.exam_file, caption="업로드된 족보", width=200)
                st.markdown("---")
                st.markdown("""
                **[분석 결과]**
                이 문제는 **'미주신경(Vagus Nerve)'**의 분포 범위를 묻고 있습니다.
                강의록 내 **<span class='highlight-text'>Parasympathetic Division</span>** 파트와 **99% 일치**합니다.
                
                **💡 출제 포인트**
                * 부교감신경의 75%를 담당한다는 점이 핵심입니다.
                * 23년, 21년 중간고사에도 유사하게 출제되었습니다.
                """, unsafe_allow_html=True)
                
                if not st.session_state.analysis_done:
                    if st.button("📌 나만의 노트로 정리 (Auto-Scrap)", type="primary"):
                        with st.spinner("핵심 요약 중..."):
                            time.sleep(1)
                            st.session_state.analysis_done = True
                            st.rerun()
                else:
                    st.success("✅ 노트 생성 및 저장 완료!")
        
        with tab2:
            st.markdown("#### 📝 Digital Consolidation")
            if st.session_state.analysis_done:
                note_html = """
                <h5>📌 [핵심 정리] 미주신경 (CN X)</h5>
                <hr>
                <b>1. 정의 및 기능</b><br>
                - 부교감신경의 75% 차지 (핵심!)<br>
                - 흉강/복강 내 장기에 광범위하게 분포함.<br><br>
                <b>2. 족보(기출) 체크 ✔️</b><br>
                - '분포 범위'를 묻는 문제가 빈출됨.<br>
                - 23년도 기출 4번과 직접 연계.<br><br>
                <b>3. 암기 팁</b><br>
                - 'Vagus' = 방랑자 (온 몸을 돌아다님)
                """
                st.markdown(f"<div class='smart-note'>{note_html}</div>", unsafe_allow_html=True)
                st.caption("🔒 Data encrypted & stored in Private Vault")
                
                st.divider()
                if st.button("📋 피드백 남기기 (Next)"):
                    st.session_state.step = 'survey'
                    st.rerun()
            else:
                st.info("👈 왼쪽 탭에서 '나만의 노트로 정리'를 눌러보세요.")

# ==========================================
# [Scene 4] 사업성 검증 설문 (데이터 수집)
# ==========================================
elif st.session_state.step == 'survey':
    st.header("📝 Product Market Fit (PMF) 검증")
    st.markdown("사업계획서의 가설을 검증하기 위한 설문입니다.")
    
    with st.form("survey_form"):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**1. Time Saving (시간 단축)**")
            st.radio("기존 학습 방식 대비, 자료 찾는 시간이 얼마나 줄어들 것 같나요?",
                     ["변화 없음", "약간 단축", "절반 단축", "85% 이상 (획기적)"])
        with c2:
            st.markdown("**2. WTP (지불 용의)**")
            st.radio("이 기능을 **월 5,900원(커피 한 잔)**에 구독하시겠습니까?",
                     ["아니오", "글쎄요", "구독함", "무조건 사전예약"])
            
        st.markdown("**3. 가장 필요한 기능은?**")
        st.multiselect("복수 선택 가능", 
                       ["RAG 족보 자동 매칭", "원클릭 스마트 스크랩", "Private Vault (보안)"])
        
        email = st.text_input("🎁 출시 알림 및 베타 테스터 신청 (이메일)")
        
        if st.form_submit_button("의견 제출 및 무료 쿠폰 받기"):
            st.balloons()
            st.success("소중한 의견 감사합니다! Med-Study OS 개발에 반영하겠습니다.")
