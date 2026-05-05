import streamlit as st
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components
import time

# ==========================================
# 1. CẤU HÌNH TRANG
# ==========================================
st.set_page_config(page_title="ED-ODYSSEY", page_icon="🚀", layout="wide")

# ==========================================
# 2. CSS CAO CẤP (MONOLITHIC CARDS & NEON UI)
# ==========================================
st.markdown("""
    <style>
    /* Nền tổng thể tối và sang trọng hơn */
    .stApp { background-color: #0A0F1C; }
    
    /* Căn chỉnh lại lề, mở rộng không gian ra 1200px để thẻ không bị ép nhỏ */
    .block-container { padding-top: 2rem; max-width: 1200px; } 

    /* Tiêu đề */
    .main-title { font-size: 2.6rem; font-weight: 900; color: #f8fafc; margin-bottom: 5px; letter-spacing: -0.5px;}
    .sub-title { color: #94a3b8; font-size: 1.1rem; margin-bottom: 35px; font-weight: 400;}

    /* =========================================
       THIẾT KẾ THẺ NGUYÊN KHỐI (MONOLITHIC CARD) 
       ========================================= */
    .cyber-card {
        background: #111827;
        border: 1px solid #1e293b;
        border-bottom: none; /* Bỏ viền đáy để ghép nối với nút */
        border-radius: 16px 16px 0 0; /* Chỉ bo tròn 2 góc trên */
        overflow: hidden;
        display: flex;
        flex-direction: column;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    /* Hiệu ứng nổi lên khi di chuột vào toàn bộ cột */
    div[data-testid="column"]:hover .cyber-card {
        border-color: #38bdf8;
        transform: translateY(-4px);
    }
    div[data-testid="column"]:hover div.stButton > button {
        transform: translateY(-4px);
        box-shadow: 0 12px 25px -5px rgba(56, 189, 248, 0.4) !important;
        filter: brightness(1.1);
    }

    /* Vùng chứa ảnh tỷ lệ 16:9 chuẩn mực */
    .img-wrapper {
        width: 100%; height: 180px; 
        border-bottom: 1px solid #1e293b;
        background-color: #0f172a;
    }
    .img-wrapper img {
        width: 100%; height: 100%; 
        object-fit: cover; /* Đảm bảo ảnh không bao giờ bị méo */
        object-position: top; /* Tập trung vào phần trên của ảnh */
    }

    /* Nội dung văn bản */
    .card-content {
        padding: 22px; 
        display: flex; flex-direction: column;
    }
    .c-title { font-size: 1.2rem; font-weight: 800; color: #f8fafc; margin-bottom: 6px; }
    .c-author { font-size: 0.75rem; color: #0ea5e9; text-transform: uppercase; font-weight: 800; letter-spacing: 0.5px; margin-bottom: 12px; }
    .c-desc { font-size: 0.85rem; color: #cbd5e1; line-height: 1.6; height: 65px; overflow: hidden;}
    .c-price { font-size: 1.4rem; font-weight: 900; color: #fff; margin-top: 15px; }

    /* NÚT BẤM ĐƯỢC "KHÂU" DÍNH VÀO THẺ */
    div.stButton > button {
        background: linear-gradient(90deg, #0284c7 0%, #0ea5e9 100%) !important;
        border: none !important; color: white !important; 
        font-weight: 800 !important; font-size: 1.05rem !important;
        border-radius: 0 0 16px 16px !important; /* Chỉ bo tròn 2 góc dưới */
        padding: 14px !important; width: 100% !important;
        margin-top: -15px !important; /* Kéo nút giật lùi lên để dính chặt vào thẻ */
        transition: all 0.3s ease !important;
    }

    /* THẺ ID BÊN SIDEBAR - HOLOGRAM EFFECT */
    .founder-pass {
        background: linear-gradient(135deg, rgba(15,23,42,0.9) 0%, rgba(30,58,138,0.7) 100%);
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 16px; padding: 22px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.6); margin-bottom: 25px;
    }
    .pass-header { font-size: 0.7rem; color: #94a3b8; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 12px; }
    .pass-balance { font-size: 2.6rem; font-weight: 900; color: #38bdf8; line-height: 1; text-shadow: 0 0 15px rgba(56,189,248,0.3);}
    .pass-currency { font-size: 1rem; color: #e2e8f0; font-weight: 500; }
    .pass-user { font-size: 0.95rem; color: #f8fafc; font-weight: 800; margin-top: 18px; letter-spacing: 1px; }
    .pass-id { font-size: 0.75rem; color: #64748b; font-family: monospace; margin-top: 5px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. KHỞI TẠO STATE & XỬ LÝ THANH TOÁN
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
# 4. SIDEBAR
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
# 5. KHU VỰC CHÍNH (MARKETPLACE / WORKSPACE)
# ==========================================

if menu == "🛒 Blueprint Marketplace":
    st.markdown('<div class="main-title">Blueprint Marketplace</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Thuê mượn và trao đổi các mô-đun công nghệ giáo dục chuyên sâu.</div>', unsafe_allow_html=True)
    
    # Rút khoảng cách gap="large" xuống "medium" để 3 thẻ giãn ra to hơn một chút
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown("""
            <div class="cyber-card">
                <div class="img-wrapper">
                    <!-- Link ảnh gốc của ông -->
                    <img src="https://i.postimg.cc/3xw93DjG/physics.png">
                </div>
                <div class="card-content">
                    <div class="c-title">Mô Phỏng Vật Lý 10</div>
                    <div class="c-author">By ED-ODYSSEY</div>
                    <div class="c-desc">Môi trường giả lập tương tác Vật Lý. Phân tích vector và động học ném xiên.</div>
                    <div class="c-price">15 CR</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mua gói vĩnh viễn", key="b1", use_container_width=True):
            process_purchase("Mô Phỏng Vật Lý 10", 15)

    with col2:
        st.markdown("""
            <div class="cyber-card">
                <div class="img-wrapper">
                    <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80">
                </div>
                <div class="card-content">
                    <div class="c-title">Đồ Thị Động Học</div>
                    <div class="c-author">By MathWiz_01</div>
                    <div class="c-desc">Thuật toán xử lý dữ liệu vận tốc. Tự động tìm cực đại, cực tiểu và vẽ gia tốc.</div>
                    <div class="c-price">10 CR</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mua gói vĩnh viễn", key="b2", use_container_width=True):
            process_purchase("Đồ Thị Động Học", 10)

    with col3:
        st.markdown("""
            <div class="cyber-card">
                <div class="img-wrapper">
                    <img src="https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=800&q=80">
                </div>
                <div class="card-content">
                    <div class="c-title">Xử Lý Tích Vô Hướng</div>
                    <div class="c-author">By CodeNinja_HN</div>
                    <div class="c-desc">Engine xử lý ma trận và cảnh báo sai sót ký hiệu Vector cho môn Toán 10.</div>
                    <div class="c-price">12 CR</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mua gói vĩnh viễn", key="b3", use_container_width=True):
            process_purchase("Xử Lý Tích Vô Hướng", 12)

elif menu == "💻 My Workspace":
    st.markdown('<div class="main-title">My Workspace</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Bàn làm việc kỹ thuật số. Chọn tab bên dưới để khởi chạy công cụ.</div>', unsafe_allow_html=True)
    
    # Kiểm tra xem người dùng đã mua món đồ nào chưa
    if not st.session_state.owned_tools:
        st.info("Workspace trống. Hãy nạp Credit và ghé Marketplace để trang bị công cụ.")
    else:
        # Tự động tạo các Tab dựa trên danh sách đồ đã mua
        tabs = st.tabs(st.session_state.owned_tools)
        
        for i, tool in enumerate(st.session_state.owned_tools):
            with tabs[i]:
                st.write("") # Tạo khoảng cách nhỏ
                
                if tool == "Mô Phỏng Vật Lý 10":
                    # Link này ông đã có sẵn
                    components.iframe("https://mo-phong-vat-ly-10.streamlit.app/?embed=true", height=800, scrolling=True)
                
                elif tool == "Đồ Thị Động Học":
                    # THAY LINK WEB ĐỒ THỊ CỦA ÔNG VÀO ĐÂY
                    # Lưu ý: Phải có đuôi /?embed=true để thanh menu của trang con bị ẩn đi
                    components.iframe("https://link-trang-do-thi-cua-ong.streamlit.app/?embed=true", height=800, scrolling=True)
                    
                elif tool == "Xử Lý Tích Vô Hướng":
                    # THAY LINK WEB VECTOR CỦA ÔNG VÀO ĐÂY
                    components.iframe("https://link-trang-vector-cua-ong.streamlit.app/?embed=true", height=800, scrolling=True)

elif menu == "🎯 Bounty Board":
    st.markdown('<div class="main-title">Bounty Board</div>', unsafe_allow_html=True)
    st.info("Bảng nhiệm vụ treo thưởng đang được bảo trì.")
