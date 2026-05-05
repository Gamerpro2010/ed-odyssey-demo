import streamlit as st
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components

# ==========================================
# 1. CẤU HÌNH TRANG & CSS (UI/UX CHUẨN EDTECH)
# ==========================================
st.set_page_config(page_title="ED-ODYSSEY | Nền tảng học tập", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    /* Reset khoảng cách mặc định để trang thoáng hơn */
    .block-container { padding-top: 2rem; max-width: 1200px; }
    
    /* Thiết kế Thẻ Sản Phẩm (Style Udemy/Coursera) */
    .course-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .course-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border-color: #3b82f6;
    }
    .course-title { font-size: 1.25rem; font-weight: 700; margin-bottom: 8px; }
    .course-author { font-size: 0.85rem; color: #6b7280; margin-bottom: 15px; display: flex; align-items: center; gap: 5px; }
    .course-desc { font-size: 0.95rem; opacity: 0.8; margin-bottom: 20px; line-height: 1.5; }
    .course-price { font-size: 1.5rem; font-weight: 800; color: #2563eb; margin-bottom: 15px; }
    
    /* Thiết kế Header của trang */
    .page-header { font-size: 2.5rem; font-weight: 800; margin-bottom: 5px; }
    .page-subheader { font-size: 1.1rem; opacity: 0.7; margin-bottom: 30px; font-weight: 400; }
    
    /* Chỉnh sửa Sidebar cho giống Dashboard chuyên nghiệp */
    [data-testid="stSidebar"] { border-right: 1px solid rgba(128, 128, 128, 0.1); }
    .wallet-box { padding: 15px; border-radius: 10px; background-color: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2); text-align: center; margin-bottom: 20px; }
    .wallet-label { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; color: #3b82f6; font-weight: 600; }
    .wallet-value { font-size: 1.8rem; font-weight: 800; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HỆ THỐNG DỮ LIỆU & LOGIC GIAO DỊCH
# ==========================================
if 'credit_balance' not in st.session_state:
    st.session_state.credit_balance = 50000 
if 'owned_tools' not in st.session_state:
    st.session_state.owned_tools = []

def process_purchase(tool_name, price):
    if tool_name in st.session_state.owned_tools:
        st.toast(f"Bạn đã sở hữu {tool_name}!", icon="ℹ️")
    elif st.session_state.credit_balance >= price:
        st.session_state.credit_balance -= price
        st.session_state.owned_tools.append(tool_name)
        st.toast(f"Đã mở khóa: {tool_name}", icon="✅")
    else:
        st.error("Số dư Credit không đủ. Vui lòng nạp thêm.")

# ==========================================
# 3. SIDEBAR (DASHBOARD NAVIGATION)
# ==========================================
with st.sidebar:
    st.markdown("### 🎓 ED-ODYSSEY")
    st.write("---")
    
    # Ví điện tử (Thiết kế tinh tế, không màu mè)
    st.markdown(f"""
        <div class="wallet-box">
            <div class="wallet-label">Số dư Credit</div>
            <div class="wallet-value">{st.session_state.credit_balance:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.popover("➕ Nạp Credit", use_container_width=True):
        st.markdown("**Chọn kênh thanh toán:**")
        method = st.selectbox("Phương thức", ["Ví MoMo", "Bank Transfer (VietQR)"], label_visibility="collapsed")
        if st.button("Xác nhận nạp 20,000 CR", type="primary", use_container_width=True):
            st.session_state.credit_balance += 20000
            st.rerun()

    st.write("---")
    st.markdown("**MENU CHÍNH**")
    menu = st.radio("Menu", ["📦 Marketplace", "💻 My Workspace", "🎯 Bounty Board"], label_visibility="collapsed")

# ==========================================
# 4. KHU VỰC CHÍNH (MAIN CONTENT)
# ==========================================

if menu == "📦 Marketplace":
    st.markdown('<div class="page-header">Blueprint Marketplace</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subheader">Khám phá các công cụ hỗ trợ học tập chuyên sâu được xây dựng bởi cộng đồng.</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    # Sản phẩm 1
    with c1:
        st.markdown(f"""
            <div class="course-card">
                <div>
                    <div class="course-title">Mô Phỏng Vật Lý 10</div>
                    <div class="course-author">🏢 Nền tảng ED-ODYSSEY</div>
                    <div class="course-desc">Môi trường giả lập tương tác chuyên sâu cho chương trình Vật Lý. Phân tích vector và động học.</div>
                </div>
                <div>
                    <div class="course-price">15,000 CR</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mở khóa bản quyền", key="buy1", use_container_width=True, type="primary"):
            process_purchase("Mô Phỏng Vật Lý 10", 15000)

    # Sản phẩm 2
    with c2:
        st.markdown(f"""
            <div class="course-card">
                <div>
                    <div class="course-title">Đồ Thị Động Học</div>
                    <div class="course-author">👤 MathWiz_01</div>
                    <div class="course-desc">Hệ thống xử lý dữ liệu vận tốc - thời gian. Tự động tìm cực đại, cực tiểu và tính toán gia tốc.</div>
                </div>
                <div>
                    <div class="course-price">10,000 CR</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mở khóa bản quyền", key="buy2", use_container_width=True, type="primary"):
            process_purchase("Đồ Thị Động Học", 10000)

    # Sản phẩm 3
    with c3:
        st.markdown(f"""
            <div class="course-card">
                <div>
                    <div class="course-title">Xử Lý Tích Vô Hướng</div>
                    <div class="course-author">👤 CodeNinja_HN</div>
                    <div class="course-desc">Thuật toán xử lý ma trận và cảnh báo sai sót ký hiệu Vector cho môn Toán hình học lớp 10.</div>
                </div>
                <div>
                    <div class="course-price">12,000 CR</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mở khóa bản quyền", key="buy3", use_container_width=True, type="primary"):
            process_purchase("Xử Lý Tích Vô Hướng", 12000)

elif menu == "💻 My Workspace":
    st.markdown('<div class="page-header">My Workspace</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subheader">Nơi truy cập các công cụ bạn đã sở hữu.</div>', unsafe_allow_html=True)
    
    if not st.session_state.owned_tools:
        st.info("Workspace của bạn đang trống. Hãy ghé Marketplace để tìm kiếm công cụ phù hợp.")
    else:
        if "Mô Phỏng Vật Lý 10" in st.session_state.owned_tools:
            st.markdown("### 🚀 Trình giả lập: Mô Phỏng Vật Lý 10")
            # Nhúng link Iframe sạch
            components.iframe("https://mo-phong-vat-ly-10.streamlit.app/?embed=true", height=800, scrolling=True)
            st.divider()
            
        if "Đồ Thị Động Học" in st.session_state.owned_tools:
            st.markdown("### 📈 Đồ Thị Động Học")
            st.success("Module đang ở trạng thái chờ nạp dữ liệu (.csv).")
            st.divider()
            
        if "Xử Lý Tích Vô Hướng" in st.session_state.owned_tools:
            st.markdown("### 🧮 Xử Lý Tích Vô Hướng")
            st.success("Engine toán học đã được khởi động.")

elif menu == "🎯 Bounty Board":
    st.markdown('<div class="page-header">Bounty Board</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subheader">Nhận nhiệm vụ từ cộng đồng để kiếm thêm Credit.</div>', unsafe_allow_html=True)
    st.info("Tính năng này đang trong giai đoạn hoàn thiện giao diện.")
