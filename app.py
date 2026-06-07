import streamlit as st
import pandas as pd
import time
from typing import List, Dict

# ==========================================
# 1. UI 및 테마 설정 (FDV 원칙: 깔끔한 여백과 명확한 타이틀)
# ==========================================
st.set_page_config(page_title="스마트 매물장 MVP", page_icon="🏠", layout="wide")

# ==========================================
# 2. Mock 데이터 및 상태 관리 초기화
# ==========================================
def init_session_state():
    """앱 새로고침 시에도 매물 데이터가 유지되도록 세션 상태 초기화"""
    if 'listings' not in st.session_state:
        st.session_state.listings = [
            {"id": "P001", "type": "아파트", "price": "매매 8.5억", "location": "서울시 강남구", "features": "올수리, 로얄층, 남향", "status": "광고중 🟢"},
            {"id": "P002", "type": "원룸", "price": "보 1000 / 월 60", "location": "서울시 관악구", "features": "풀옵션, 역세권 3분", "status": "광고중 🟢"},
            {"id": "P003", "type": "오피스텔", "price": "전세 2.2억", "location": "서울시 마포구", "features": "신축 첫입주, 주차편리", "status": "광고중 🟢"},
            {"id": "P004", "type": "상가", "price": "보 5000 / 월 300", "location": "서울시 성동구", "features": "무권리, 코너자리, 1층", "status": "거래완료 🔴"}
        ]

init_session_state()

# ==========================================
# 3. 비즈니스 로직 함수 (가짜 AI 및 자동화 딜레이)
# ==========================================
def terminate_ads(selected_ids: List[str]):
    """선택된 매물들의 상태를 '거래완료'로 변경 (자동화 매크로 시뮬레이션)"""
    for item in st.session_state.listings:
        if item['id'] in selected_ids:
            item['status'] = "거래완료 🔴"

def generate_blog_text(listing: Dict) -> str:
    """선택된 매물 데이터를 바탕으로 블로그 텍스트 생성 (LLM 시뮬레이션)"""
    # 📘 ISLP, p.403 (NLP 텍스트 생성 개념 적용)
    text = f"""
    ### ✨ [급매/추천] {listing['location']} 최고의 {listing['type']} 소개합니다! ✨
    
    안녕하세요! 오늘 소개해 드릴 정말 귀한 매물은 바로 **{listing['location']}**에 위치한 **{listing['type']}**입니다. 
    요즘 이 지역에서 이만한 조건 찾기 정말 힘든 거 아시죠? 😅
    
    **💡 매물 핵심 정보**
    - **가격:** {listing['price']}
    - **특장점:** {listing['features']}
    
    특히 **{listing['features'].split(',')[0]}** 조건이 너무 좋아서 실거주나 투자 목적으로 모두 강력 추천드립니다. 
    빠른 거래가 예상되니 주저하지 마시고 지금 바로 연락주세요! 📞
    """
    return text

# ==========================================
# 4. 프론트엔드 화면 구성 (Tabs)
# ==========================================
st.title("🏠 스마트 매물장 & 마케팅 자동화 (MVP)")
st.markdown("공인중개사 업무 효율 향상을 위한 통합 관리 시스템 프로토타입입니다.")

# 탭 생성
tab1, tab2 = st.tabs(["📋 매물 관리 및 광고 종료", "✍️ AI 블로그 자동 생성"])

# ------------------------------------------
# [탭 1] 매물 관리 및 일괄 종료
# ------------------------------------------
with tab1:
    st.subheader("현재 등록된 매물 목록")
    
    # 데이터프레임 시각화
    df = pd.DataFrame(st.session_state.listings)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # 폼(Form)을 이용한 동작 제어
    with st.form("terminate_form"):
        st.write("#### 🛑 원클릭 인터넷 광고 일괄 종료")
        
        # 현재 광고중인 매물만 필터링하여 다중 선택창에 표시
        active_listings = [item for item in st.session_state.listings if "광고중" in item['status']]
        active_options = {f"{item['id']} - {item['type']} ({item['location']})": item['id'] for item in active_listings}
        
        selected_titles = st.multiselect(
            "거래 완료된 매물을 선택하세요 (다중 선택 가능):", 
            options=list(active_options.keys())
        )
        
        submit_terminate = st.form_submit_button("선택 매물 광고 일괄 종료 🚀")
        
        if submit_terminate:
            if not selected_titles:
                st.warning("종료할 매물을 먼저 선택해 주세요.")
            else:
                with st.spinner("네이버 부동산, 직방 등 플랫폼 접속 및 광고 종료 처리 중... (가상 대기)"):
                    time.sleep(2) # 매크로 작동 시간 시뮬레이션
                    selected_ids = [active_options[t] for t in selected_titles]
                    terminate_ads(selected_ids)
                st.success(f"성공적으로 {len(selected_titles)}건의 광고를 종료했습니다! (페이지가 갱신됩니다)")
                time.sleep(1)
                st.rerun() # 상태 업데이트 후 화면 새로고침

# ------------------------------------------
# [탭 2] AI 블로그 텍스트 생성
# ------------------------------------------
with tab2:
    st.subheader("🤖 매물 데이터 기반 홍보글 원클릭 작성")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("**1. 홍보할 매물 선택**")
        all_options = {f"{item['id']} - {item['type']}": item for item in st.session_state.listings}
        selected_target = st.selectbox("블로그 글을 작성할 매물을 고르세요:", options=list(all_options.keys()))
        
        generate_btn = st.button("블로그 글 생성하기 🪄", type="primary")
        
    with col2:
        st.write("**2. AI 생성 결과 (미리보기 및 복사)**")
        if generate_btn:
            with st.spinner("최신 마케팅 트렌드를 분석하여 매력적인 글을 작성하고 있습니다..."):
                time.sleep(1.5) # AI 생성 시간 시뮬레이션
                target_listing = all_options[selected_target]
                generated_result = generate_blog_text(target_listing)
                
            # 생성된 텍스트 출력
            st.info("작성이 완료되었습니다. 아래 텍스트를 복사하여 블로그에 바로 붙여넣으세요.")
            st.text_area("생성된 본문", value=generated_result, height=300)
        else:
            st.text_area("생성된 본문", value="매물을 선택하고 [생성하기] 버튼을 누르세요.", height=300, disabled=True)