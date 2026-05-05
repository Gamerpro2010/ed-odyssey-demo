import streamlit as st
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components
import time

# ==========================================
# 1. CẤU HÌNH TRANG & CSS (CYBER-GLASS UI)
# ==========================================
st.set_page_config(page_title="ED-ODYSSEY", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    /* Bố cục tổng thể thoáng hơn */
    .block-container { padding-top: 1.5rem; max-width: 1200px; }
    
    /* 1. THIẾT KẾ THẺ ID Ở SIDEBAR (ĐẶC BIỆT) */
    .founder-pass {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 58, 138, 0.9) 100%);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 20px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        margin-bottom: 25px;
    }
    .founder-pass::after {
        content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
        background: linear-gradient(to right, transparent, rgba(255,255,255,0.1), transparent);
        transform: skewX(-20deg); animation: shine 4s infinite;
    }
    @keyframes shine { 0% {left: -100%;} 20% {left: 200%;} 100% {left: 200%;} }
    
    .pass-header { font-size: 0.7rem; color: #94a3b8; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 10px; }
    .pass-balance { font-size: 2.5rem; font-weight: 900; color: #38bdf8; line-height: 1; text-shadow: 0 0 10px rgba(56,189,248,0.4); }
    .pass-currency { font-size: 1rem; color: #e2e8f0; }
    .pass-user { font-size: 0.9rem; color: #f8fafc; font-weight: 700; margin-top: 15px; letter-spacing: 1px; }
    .pass-id { font-size: 0.65rem; color: #64748b; font-family: monospace; }

    /* 2. THIẾT KẾ CARD SẢN PHẨM Ở MARKETPLACE */
    .cyber-card {
        background-color: #0f172a;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #1e293b;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 15px;
    }
    .cyber-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(56, 189, 248, 0.15);
        border-color: #38bdf8;
    }
    .card-img {
        width: 100%; height: 150px; object-fit: cover;
        border-bottom: 1px solid #1e293b;
    }
    .card-content { padding: 15px; }
    .c-title { font-size: 1.2rem; font-weight: 800; color: #f8fafc; margin-bottom: 5px; }
    .c-author { font-size: 0.75rem; color: #38bdf8; font-weight: 600; text-transform: uppercase; margin-bottom: 10px; }
    .c-desc { font-size: 0.85rem; color: #94a3b8; line-height: 1.5; height: 60px; overflow: hidden; margin-bottom: 15px; }
    .c-footer { display: flex; justify-content: space-between; align-items: center; border-top: 1px dashed #334155; padding-top: 15px; }
    .c-price { font-size: 1.2rem; font-weight: 800; color: #fff; }

    /* 3. ĐỔI MÀU NÚT BẤM (Xóa màu đỏ, dùng Gradient Xanh) */
    button[kind="primary"] {
        background: linear-gradient(90deg, #2563eb 0%, #38bdf8 100%) !important;
        border: none !important; color: white !important; font-weight: 700 !important;
        border-radius: 6px !important; transition: 0.3s !important;
    }
    button[kind="primary"]:hover { opacity: 0.9; box-shadow: 0 0 15px rgba(56,189,248,0.5) !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. KHỞI TẠO STATE HỆ THỐNG
# ==========================================
if 'credit_balance' not in st.session_state:
    st.session_state.credit_balance = 50 
if 'owned_tools' not in st.session_state:
    st.session_state.owned_tools = []

def process_purchase(tool_name, price):
    if tool_name in st.session_state.owned_tools:
        st.toast(f"Bạn đã sở hữu {tool_name}!", icon="ℹ️")
    elif st.session_state.credit_balance >= price:
        st.session_state.credit_balance -= price
        st.session_state.owned_tools.append(tool_name)
        st.toast(f"Mở khóa thành công: {tool_name}", icon="✅")
        st.balloons()
    else:
        st.error("Số dư Credit không đủ!")

# ==========================================
# 3. SIDEBAR (HỆ THỐNG ĐIỀU HƯỚNG MỚI)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1162/1162846.png", width=50)
    st.write("---")
    
    # Thẻ ID Cá nhân hóa siêu ngầu
    st.markdown(f"""
        <div class="founder-pass">
            <div class="pass-header">Hệ thống Ody-Credit</div>
            <div class="pass-balance">{st.session_state.credit_balance} <span class="pass-currency">CR</span></div>
            <div class="pass-user">HỒ NAM SƠN</div>
            <div class="pass-id">ID: 10QT2-FOUNDER</div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.popover("💳 Nạp Năng Lượng (CR)", use_container_width=True):
        st.markdown("**Tỷ giá: 1.000 VNĐ = 1 CR**")
        method = st.selectbox("Phương thức", ["Ví MoMo", "Chuyển khoản"])
        amount = st.number_input("Số CR muốn nạp", min_value=10, step=10, value=20)
        st.info(f"Thanh toán {amount * 1000:,} VNĐ qua {method}.")
        if st.checkbox("Xác nhận đã chuyển khoản"):
            if st.button("Xử lý giao dịch", type="primary", use_container_width=True):
                with st.spinner("Đang kết nối ngân hàng..."):
                    time.sleep(1)
                    st.session_state.credit_balance += amount
                    st.rerun()

    st.write("---")
    menu = st.radio("ĐIỀU HƯỚNG", ["🛒 Blueprint Marketplace", "💻 My Workspace", "🎯 Bounty Board"], label_visibility="collapsed")

# ==========================================
# 4. KHU VỰC CHÍNH (MARKETPLACE / WORKSPACE)
# ==========================================

if menu == "🛒 Blueprint Marketplace":
    st.title("Blueprint Marketplace")
    st.markdown("Thuê mượn và trao đổi các mô-đun công nghệ giáo dục chuyên sâu.")
    st.write("")
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown("""
            <div class="cyber-card">
                <img src="https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?auto=format&fit=crop&w=500&q=80" class="card-img">
                <div class="card-content">
                    <div class="c-title">Mô Phỏng Vật Lý 10</div>
                    <div class="c-author">By ED-ODYSSEY</div>
                    <div class="c-desc">Môi trường giả lập tương tác Vật Lý. Phân tích vector và động học ném xiên thời gian thực.</div>
                    <div class="c-footer">
                        <div class="c-price">15 CR</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mua gói vĩnh viễn", key="b1", use_container_width=True, type="primary"):
            process_purchase("Mô Phỏng Vật Lý 10", 15)

    with col2:
        st.markdown("""
            <div class="cyber-card">
                <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=500&q=80" class="card-img">
                <div class="card-content">
                    <div class="c-title">Đồ Thị Động Học</div>
                    <div class="c-author">By MathWiz_01</div>
                    <div class="c-desc">Thuật toán xử lý dữ liệu vận tốc - thời gian. Tự động tìm cực đại, cực tiểu và vẽ gia tốc.</div>
                    <div class="c-footer">
                        <div class="c-price">10 CR</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mua gói vĩnh viễn", key="b2", use_container_width=True, type="primary"):
            process_purchase("Đồ Thị Động Học", 10)

    with col3:
        st.markdown("""
            <div class="cyber-card">
                <img src="https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=500&q=80" class="card-img">
                <div class="card-content">
                    <div class="c-title">Xử Lý Tích Vô Hướng</div>
                    <div class="c-author">By CodeNinja_HN</div>
                    <div class="c-desc">Engine xử lý ma trận và cảnh báo sai sót ký hiệu Vector cho môn Toán hình học lớp 10.</div>
                    <div class="c-footer">
                        <div class="c-price">12 CR</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mua gói vĩnh viễn", key="b3", use_container_width=True, type="primary"):
            process_purchase("Xử Lý Tích Vô Hướng", 12)

elif menu == "💻 My Workspace":
    st.title("My Workspace")
    st.write("Bàn làm việc kỹ thuật số. Chọn tab bên dưới để khởi chạy công cụ.")
    st.write("")
    
    if not st.session_state.owned_tools:
        st.info("Workspace trống. Hãy nạp Credit và ghé Marketplace để trang bị công cụ.")
    else:
        tabs = st.tabs(st.session_state.owned_tools)
        
        for i, tool in enumerate(st.session_state.owned_tools):
            with tabs[i]:
                st.write("")
                if tool == "Mô Phỏng Vật Lý 10":
                    components.iframe("https://mo-phong-vat-ly-10.streamlit.app/?embed=true", height=750, scrolling=True)
                elif tool == "Đồ Thị Động Học":
                    st.success("Hệ thống phân tích Pandas/NumPy đã sẵn sàng.")
                    st.file_uploader("Tải tệp dữ liệu thí nghiệm (.csv)", type=['csv'])
                elif tool == "Xử Lý Tích Vô Hướng":
                    c_left, c_right = st.columns(2)
                    c_left.text_input("Tọa độ Vector U:")
                    c_right.text_input("Tọa độ Vector V:")
                    st.button("Tính toán", type="primary")

elif menu == "🎯 Bounty Board":
    st.title("Bounty Board")
    st.info("Bảng nhiệm vụ treo thưởng đang được bảo trì.")
