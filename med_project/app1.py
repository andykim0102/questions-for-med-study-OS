import streamlit as st
import time
import random

# --- 페이지 설정 ---
st.set_page_config(layout="wide", page_title="Med-Study OS Pro", page_icon="🧠")

# --- 세션 상태 초기화 ---
if 'step' not in st.session_state: st.session_state.step = 'dashboard'
if 'analyzing' not in st.session_state: st.session_state.analyzing = False

# --- 고급 스타일링 (CSS) ---
st.markdown("""
<style>
    /* 전체 폰트 및 배경 */
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }
    .stApp { background-color: #f4f6f9; }
    
    /* 카드 디자인 */
    .card {
        background-color: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
    }
    
    /* AI 분석 로그창 */
    .log-box {
        font-family: 'Courier New', monospace; font-size: 12px; color: #00d26a;
        background-color: #1e1e1e; padding: 10px; border-radius: 8px;
        height: 100px; overflow-y: scroll; border: 1px solid #333;
    }
    
    /* 나만의 노트 디자인 */
    .smart-note {
        background-color: #fff9c4; /* 포스트잇 색상 */
        padding: 25px; border-radius: 5px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        border-left: 5px solid #fbc02d;
        font-family: 'Gaegu', cursive; /* 손글씨 느낌 (시스템 폰트 대체) */
    }
    
    /* 하이라이트 효과 */
    .highlight { background-color: #e3f2fd; color: #1565c0; padding: 2px 5px; border-radius: 4px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [Scene 1] 메인 대시보드 (학습 현황)
# ==========================================
if st.session_state.step == 'dashboard':
    st.title("🧠 Med-Study OS: Intelligent Workspace")
    st.caption("Ver 2.1.0 Pro | Connected to SNU_Medical_DB")
    
    # 상단 지표 (있어 보이는 통계)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔥 이번 주 절약 시간", "4시간 12분", "+85%")
    c2.metric("📚 디지털 단권화", "142건", "+12건 Today")
    c3.metric("🎯 족보 매칭 정확도", "94.2%", "+1.5%")
    c4.metric("📅 시험 D-Day", "D-14", "해부학")
    
    st.divider()
    
    # 자료 업로드 섹션
    st.markdown("### 📂 New Study Session")
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            st.info("Step 1. 학습할 강의 자료 (PDF/IMG)")
            lec_file = st.file_uploader("강의록 업로드", type=['png', 'jpg', 'pdf'], key="lec")
        with col_u2:
            st.warning("Step 2. 분석할 기출 문제 (IMG)")
            exam_file = st.file_uploader("족보/기출 업로드", type=['png', 'jpg'], key="exam")
        st.markdown("</div>", unsafe_allow_html=True)

    if lec_file and exam_file:
        st.session_state.lec_file = lec_file
        st.session_state.exam_file = exam_file
        if st.button("🚀 AI Deep Analysis 시작", type="primary", use_container_width=True):
            st.session_state.step = 'processing'
            st.rerun()

# ==========================================
# [Scene 2] AI 분석 시뮬레이션 (Acting)
# ==========================================
elif st.session_state.step == 'processing':
    st.title("⚙️ Analyzing Context...")
    
    col_visual, col_log = st.columns([1, 1])
    
    with col_visual:
        st.image(st.session_state.lec_file, caption="Source Document", width=300)
    
    with col_log:
        st.markdown("### 📡 Engine Status")
        status_text = st.empty()
        prog_bar = st.progress(0)
        log_area = st.empty()
        
        logs = [
            "Initializing OCR Engine...",
            "Extracting text layers from PDF...",
            "Vectorizing content (Dimensions: 1536)...",
            "Accessing Medical Knowledge Graph...",
            "Identifying Key Concepts: 'Vagus Nerve', 'Parasympathetic'...",
            "Matching with Past Exam Database (Year: 2021-2024)...",
            "Calculating Relevance Score: 98.4%...",
            "Generating Smart Summary..."
        ]
        
        log_history = ""
        for i, log in enumerate(logs):
            time.sleep(random.uniform(0.3, 0.8))
            prog_bar.progress((i + 1) * 12)
            log_history += f"> [SYSTEM] {log}\n"
            log_area.markdown(f"<div class='log-box'>{log_history}</div>", unsafe_allow_html=True)
        
        st.success("✅ Analysis Complete!")
        time.sleep(1)
        st.session_state.step = 'result'
        st.rerun()

# ==========================================
# [Scene 3] 결과 워크스페이스 (Smart View)
# ==========================================
elif st.session_state.step == 'result':
    # 상단 헤더
    st.markdown("### 🎓 Smart Study Workspace")
    
    # 3단 레이아웃: 강의록(좌) - AI분석(중) - 노트(우)
    col_lec, col_ai, col_note = st.columns([2, 1.5, 1.5])
    
    # 1. 강의록 뷰어 (매칭 표시)
    with col_lec:
        st.markdown("**📄 Lecture Note (Source)**")
        st.image(st.session_state.lec_file, use_container_width=True)
        st.caption("✅ AI has highlighted relevant sections.")

    # 2. AI 분석 인사이트
    with col_ai:
        st.markdown("**🤖 AI Insight**")
        with st.container():
            st.markdown("<div class='card' style='border-left: 5px solid #29b6f6;'>", unsafe_allow_html=True)
            st.markdown("#### 🔍 기출 연계 분석")
            st.image(st.session_state.exam_file, width=200)
            st.markdown("---")
            st.markdown("""
            **[분석 결과]**
            이 문제는 **'미주신경(CN X)'**의 기능적 분포를 묻고 있습니다. 
            강의록 내 **<span class='highlight'>Parasympathetic Division</span>** 섹션과 **99.8% 일치**합니다.
            
            **💡 출제 포인트**
            교수님이 수업 중 *"부교감 신경의 75%는 미주신경이 담당한다"*고 3회 강조하셨습니다.
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            if st.button("✨ 나만의 정리본 생성 (Generate Note)", type="primary"):
                with st.spinner("AI가 요약 노트를 작성 중입니다..."):
                    time.sleep(1.5)
                    st.session_state.note_generated = True

    # 3. 나만의 스마트 노트 (하이라이트)
    with col_note:
        st.markdown("**📒 My Smart Note**")
        
        if 'note_generated' in st.session_state:
            # 노트가 타이핑되는 효과 연출
            note_content = """
            ### 📌 [핵심 정리] 미주신경 (CN X)
            
            **1. 핵심 개념**
            * **기능:** 부교감신경의 **75%**를 차지함 (가장 중요!)
            * **분포:** 흉강 및 복강 내 장기 대부분에 분포.
            
            **2. 족보(기출) 포인트** ⭐️
            * 23년도, 21년도 중간고사에 연속 출제됨.
            * "부교감신경의 주된 신경"을 묻는 문제로 변형 가능.
            
            **3. 암기 팁 (Mnemonic)**
            * **"Vagus"**는 라틴어로 '방랑자' → 온 몸(장기)을 돌아다님!
            """
            st.markdown(f"<div class='smart-note'>{note_content}</div>", unsafe_allow_html=True)
            st.success("💾 Private Vault에 자동 저장되었습니다.")
            
            st.markdown("---")
            if st.button("📋 만족도 설문조사 (Feedback)"):
                st.session_state.step = 'survey'
                st.rerun()
        else:
            st.info("👈 '나만의 정리본 생성' 버튼을 눌러보세요.")

# ==========================================
# [Scene 4] 사업성 검증 설문
# ==========================================
elif st.session_state.step == 'survey':
    st.title("📝 Service Validation")
    st.progress(100)
    
    with st.form("validation"):
        st.subheader("방금 경험하신 'AI 분석 및 자동 정리' 기능, 어떠셨나요?")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**1. Time Saving**")
            st.radio("기존 방식(자료 대조) 대비 시간이 얼마나 단축될 것 같나요?",
                     ["변화 없음", "약간 단축", "절반 이상 단축", "획기적임 (85% 이상)"])
        with c2:
            st.markdown("**2. Willingness to Pay**")
            st.radio("이 기능을 월 5,900원에 구독하시겠습니까?", 
                     ["아니오", "고민됨", "구독함", "무조건 구독 (사전예약)"])
            
        st.markdown("**3. 가장 인상 깊었던 기능은?**")
        st.multiselect("복수 선택 가능", 
                       ["AI 기출 연계 분석", "고퀄리티 정리본 자동 생성", "실시간 분석 연출"])
        
        if st.form_submit_button("제출 및 베타 테스터 신청"):
            st.balloons()
            st.success("소중한 의견 감사합니다. Med-Study OS 팀 드림.")
