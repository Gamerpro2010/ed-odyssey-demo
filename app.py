import streamlit as st
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components
import time

# ==========================================
# 1. CẤU HÌNH TRANG & CSS (GIAO DIỆN CYBER CHUẨN MỰC)
# ==========================================
st.set_page_config(page_title="ED-ODYSSEY", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; max-width: 1200px; }
    
    /* Thẻ ID Sidebar */
    .founder-pass {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 58, 138, 0.9) 100%);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        margin-bottom: 20px;
    }
    .pass-header { font-size: 0.7rem; color: #94a3b8; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 10px; }
    .pass-balance { font-size: 2.5rem; font-weight: 900; color: #38bdf8; line-height: 1; }
    .pass-currency { font-size: 1rem; color: #e2e8f0; }
    .pass-user { font-size: 0.9rem; color: #f8fafc; font-weight: 700; margin-top: 15px; letter-spacing: 1px; }
    .pass-id { font-size: 0.65rem; color: #64748b; font-family: monospace; }

    /* THIẾT KẾ CARD */
    .cyber-card {
        background-color: #0f172a;
        border-radius: 12px 12px 0 0; 
        overflow: hidden;
        border: 1px solid #1e293b;
        border-bottom: none; 
    }
    .card-img { width: 100%; height: 160px; object-fit: cover; display: block; border-bottom: 1px solid #1e293b; }
    .card-content { padding: 15px; }
    .c-title { font-size: 1.1rem; font-weight: 800; color: #f8fafc; margin-bottom: 5px; }
    .c-author { font-size: 0.75rem; color: #38bdf8; font-weight: 600; text-transform: uppercase; margin-bottom: 10px; }
    .c-desc { font-size: 0.85rem; color: #94a3b8; line-height: 1.5; height: 60px; overflow: hidden; margin-bottom: 15px; }
    .c-price { font-size: 1.2rem; font-weight: 800; color: #fff; border-top: 1px dashed #334155; padding-top: 10px;}

    /* NÚT BẤM KÉO SÁT VÀO CARD */
    div.stButton > button {
        background: linear-gradient(90deg, #2563eb 0%, #38bdf8 100%) !important;
        border: none !important; color: white !important; font-weight: 700 !important;
        border-radius: 0 0 12px 12px !important; 
        width: 100% !important;
        margin-top: -15px !important; 
        transition: 0.3s !important;
    }
    div.stButton > button:hover { filter: brightness(1.1); box-shadow: 0 10px 15px rgba(56,189,248,0.2) !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. KHỞI TẠO STATE & XỬ LÝ THANH TOÁN
# ==========================================
if 'credit_balance' not in st.session_state:
    st.session_state.credit_balance = 50 
if 'owned_tools' not in st.session_state:
    st.session_state.owned_tools = []
if 'show_success' not in st.session_state:
    st.session_state.show_success = None

if st.session_state.show_success:
    st.toast(f"Mở khóa thành công: {st.session_state.show_success}", icon="✅")
    st.balloons()
    st.session_state.show_success = None

def process_purchase(tool_name, price):
    if tool_name in st.session_state.owned_tools:
        st.toast(f"Bạn đã sở hữu {tool_name}!", icon="ℹ️")
    elif st.session_state.credit_balance >= price:
        st.session_state.credit_balance -= price
        st.session_state.owned_tools.append(tool_name)
        st.session_state.show_success = tool_name
        st.rerun() 
    else:
        st.error("Số dư Credit không đủ!")

# ==========================================
# 3. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("## 🚀 ED-ODYSSEY")
    st.write("---")
    
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
                <!-- VỊ TRÍ SỐ 1: CHỖ ĐỂ ÔNG DÁN LINK ẢNH CỦA ÔNG -->
                <img src="https://images.unsplash.com/photo-1614729939124-032f0b56c9ce?auto=format&fit=crop&w=800&q=80" class="card-img">
                <div class="card-content">
                    <div class="c-title">Mô Phỏng Vật Lý 10</div>
                    <div class="c-author">By ED-ODYSSEY</div>
                    <div class="c-desc">Môi trường giả lập tương tác Vật Lý. Phân tích vector và động học ném xiên.</div>
                    <div class="c-price">15 CR</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mua gói vĩnh viễn", key="b1", use_container_width=True, type="primary"):
            process_purchase("Mô Phỏng Vật Lý 10", 15)

    with col2:
        st.markdown("""
            <div class="cyber-card">
                <!-- Ảnh Đồ thị tone Dark Neon -->
                <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80" class="card-img">
                <div class="card-content">
                    <div class="c-title">Đồ Thị Động Học</div>
                    <div class="c-author">By MathWiz_01</div>
                    <div class="c-desc">Thuật toán xử lý dữ liệu vận tốc. Tự động tìm cực đại, cực tiểu và vẽ gia tốc.</div>
                    <div class="c-price">10 CR</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mua gói vĩnh viễn", key="b2", use_container_width=True, type="primary"):
            process_purchase("Đồ Thị Động Học", 10)

    with col3:
        st.markdown("""
            <div class="cyber-card">
                <!-- Ảnh Ma trận/Thuật toán -->
                <img src="https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=800&q=80" class="card-img">
                <div class="card-content">
                    <div class="c-title">Xử Lý Tích Vô Hướng</div>
                    <div class="c-author">By CodeNinja_HN</div>
                    <div class="c-desc">Engine xử lý ma trận và cảnh báo sai sót ký hiệu Vector cho môn Toán 10.</div>
                    <div class="c-price">12 CR</div>
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
