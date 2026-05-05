import streamlit as st
import streamlit.components.v1 as components
import time

# ==========================================
# 1. CẤU HÌNH TRANG
# ==========================================
st.set_page_config(page_title="ED-ODYSSEY", page_icon="🚀", layout="wide")

# ==========================================
# 2. CSS CAO CẤP: GIAO DIỆN NGUYÊN KHỐI (MONOLITHIC)
# ==========================================
st.markdown("""
    <style>
    /* Nền sẫm sang trọng */
    .stApp { background-color: #0B0F19; }
    
    /* Thu gọn lề để bố cục cân đối hơn */
    .block-container { padding-top: 2rem; max-width: 1100px; }

    /* Tiêu đề Glow nhẹ */
    .main-title { 
        font-size: 2.8rem; font-weight: 900; color: #f8fafc; 
        margin-bottom: 5px; text-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
    }
    .sub-title { color: #94a3b8; font-size: 1.1rem; margin-bottom: 40px; }

    /* THIẾT KẾ THẺ NGUYÊN KHỐI */
    .cyber-card {
        background: #111827;
        border: 1px solid #1e293b;
        border-bottom: none; /* Bỏ viền đáy để ghép với nút */
        border-radius: 16px 16px 0 0;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        height: 380px;
        transition: all 0.3s ease;
    }
    
    /* Hiệu ứng Hover cho cả cụm (Thẻ + Nút) */
    div[data-testid="column"]:hover .cyber-card {
        border-color: #38bdf8;
        transform: translateY(-5px);
    }
    div[data-testid="column"]:hover div.stButton > button {
        transform: translateY(-5px);
        filter: brightness(1.1);
        box-shadow: 0 10px 20px rgba(56, 189, 248, 0.3) !important;
    }

    .img-wrapper { width: 100%; height: 180px; overflow: hidden; border-bottom: 1px solid #1e293b; }
    .img-wrapper img { width: 100%; height: 100%; object-fit: cover; }

    .card-content { padding: 22px; flex-grow: 1; display: flex; flex-direction: column; }
    .c-title { font-size: 1.25rem; font-weight: 800; color: #f8fafc; margin-bottom: 5px; }
    .c-author { font-size: 0.75rem; color: #38bdf8; font-weight: 700; text-transform: uppercase; margin-bottom: 15px; }
    .c-desc { font-size: 0.85rem; color: #94a3b8; line-height: 1.6; }
    .c-price { font-size: 1.4rem; font-weight: 900; color: #fff; margin-top: auto; }

    /* NÚT BẤM "KHÂU" DÍNH VÀO ĐÁY THẺ */
    div.stButton > button {
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%) !important;
        border: none !important; color: white !important;
        font-weight: 800 !important; font-size: 1rem !important;
        border-radius: 0 0 16px 16px !important; /* Bo góc dưới */
        padding: 15px !important; width: 100% !important;
        margin-top: -15px !important; /* Kéo nút dính chặt vào thẻ */
        transition: all 0.3s ease !important;
    }

    /* THẺ ID SIDEBAR - CHUẨN FOUNDER */
    .founder-pass {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 16px; padding: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5); margin-bottom: 25px;
    }
    .pass-balance { font-size: 2.8rem; font-weight: 900; color: #38bdf8; line-height: 1; }
    .pass-user { font-size: 1rem; color: #f8fafc; font-weight: 800; margin-top: 15px; letter-spacing: 1px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LOGIC HỆ THỐNG
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
            <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 10px;">Ody-Credit Balance</div>
            <div class="pass-balance">{st.session_state.credit_balance} <span style="font-size: 1rem; color: #cbd5e1;">CR</span></div>
            <div class="pass-user">HỒ NAM SƠN</div>
            <div style="font-size: 0.7rem; color: #64748b; font-family: monospace;">ID: 10QT2-FOUNDER</div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.popover("💳 Nạp Credit", use_container_width=True):
        amount = st.number_input("Số CR", min_value=10, step=10, value=20)
        if st.button("Xác nhận nạp", type="primary", use_container_width=True):
            st.session_state.credit_balance += amount
            st.rerun()

    st.write("---")
    menu = st.radio("ĐIỀU HƯỚNG", ["🛒 Blueprint Marketplace", "💻 My Workspace", "🎯 Bounty Board"], label_visibility="collapsed")

# ==========================================
# 5. KHU VỰC CHÍNH
# ==========================================

if menu == "🛒 Blueprint Marketplace":
    st.markdown('<div class="main-title">Blueprint Marketplace</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Thuê mượn và trao đổi các mô-đun công nghệ giáo dục chuyên sâu.</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown(f"""
            <div class="cyber-card">
                <div class="img-wrapper"><img src="https://i.postimg.cc/3xw93DjG/physics.png"></div>
                <div class="card-content">
                    <div>
                        <div class="c-title">Mô Phỏng Vật Lý 10</div>
                        <div class="c-author">By ED-ODYSSEY</div>
                        <div class="c-desc">Giả lập tương tác Vật Lý. Phân tích vector và động học ném xiên.</div>
                    </div>
                    <div class="c-price">15 CR</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mua gói vĩnh viễn", key="b1", use_container_width=True):
            process_purchase("Mô Phỏng Vật Lý 10", 15)

    with col2:
        st.markdown(f"""
            <div class="cyber-card">
                <div class="img-wrapper"><img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80"></div>
                <div class="card-content">
                    <div>
                        <div class="c-title">Đồ Thị Động Học</div>
                        <div class="c-author">By MATHWIZ_01</div>
                        <div class="c-desc">Xử lý dữ liệu vận tốc. Tự động tìm cực trị và vẽ gia tốc nhanh chóng.</div>
                    </div>
                    <div class="c-price">10 CR</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mua gói vĩnh viễn", key="b2", use_container_width=True):
            process_purchase("Đồ Thị Động Học", 10)

    with col3:
        st.markdown(f"""
            <div class="cyber-card">
                <div class="img-wrapper"><img src="https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=800&q=80"></div>
                <div class="card-content">
                    <div>
                        <div class="c-title">Xử Lý Tích Vô Hướng</div>
                        <div class="c-author">By CODENINJA_HN</div>
                        <div class="c-desc">Engine xử lý ma trận và cảnh báo sai sót ký hiệu Vector cho Toán 10.</div>
                    </div>
                    <div class="c-price">12 CR</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mua gói vĩnh viễn", key="b3", use_container_width=True):
            process_purchase("Xử Lý Tích Vô Hướng", 12)

elif menu == "💻 My Workspace":
    st.markdown('<div class="main-title">My Workspace</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Bàn làm việc kỹ thuật số. Chọn tab bên dưới để khởi chạy công cụ.</div>', unsafe_allow_html=True)
    
    if not st.session_state.owned_tools:
        st.info("Bàn làm việc của ông đang trống. Hãy ghé Marketplace để trang bị thêm công cụ!")
    else:
        # Tự động tạo Tab dựa trên danh sách đồ đã mua
        tabs = st.tabs(st.session_state.owned_tools)
        
        for i, tool in enumerate(st.session_state.owned_tools):
            with tabs[i]:
                st.write("") 
                if tool == "Mô Phỏng Vật Lý 10":
                    components.iframe("https://mo-phong-vat-ly-10.streamlit.app/?embed=true", height=850, scrolling=True)
                elif tool == "Đồ Thị Động Học":
                    # THAY LINK WEB ĐỒ THỊ CỦA ÔNG VÀO ĐÂY SAU KHI DEPLOY XONG
                    components.iframe("https://kinematics-lab-demo.streamlit.app/?embed=true", height=850, scrolling=True)
                elif tool == "Xử Lý Tích Vô Hướng":
                    # THAY LINK WEB VECTOR CỦA ÔNG VÀO ĐÂY SAU KHI DEPLOY XONG
                    components.iframe("https://vector-engine-demo.streamlit.app/?embed=true", height=850, scrolling=True)
