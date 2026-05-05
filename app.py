import streamlit as st

# ==========================================
# 1. CẤU HÌNH TRANG & GIAO DIỆN (UI/UX)
# ==========================================
st.set_page_config(
    page_title="ED-ODYSSEY | Blueprint Marketplace",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS phong cách SaaS/Fintech chuyên nghiệp
st.markdown("""
    <style>
    /* Ẩn các thành phần mặc định không cần thiết của Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Thiết kế thẻ Ví tiền (Wallet) trên Sidebar */
    .wallet-card {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2);
        margin-bottom: 25px;
    }
    .wallet-title { font-size: 13px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9; margin-bottom: 5px; }
    .wallet-amount { font-size: 28px; font-weight: 800; letter-spacing: 0.5px; }

    /* Tiêu đề chính của trang */
    .market-title { font-size: 2.2rem; font-weight: 800; color: #1e40af; margin-bottom: 0px; padding-bottom: 0px; }
    .market-subtitle { font-size: 1.2rem; font-weight: 600; color: #3b82f6; margin-top: 5px; margin-bottom: 5px; }
    .market-desc { font-size: 0.95rem; color: #64748b; margin-bottom: 30px; }

    /* Badge tên Creator */
    .creator-badge {
        display: inline-block;
        background-color: rgba(59, 130, 246, 0.1);
        color: #2563eb;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 15px;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. KHỞI TẠO STATE & XỬ LÝ LOGIC
# ==========================================
if 'balance' not in st.session_state:
    st.session_state.balance = 50000

# Hàm xử lý mua hàng giả lập
def handle_purchase(price, item_name):
    if st.session_state.balance >= price:
        st.session_state.balance -= price
        st.toast(f"Giao dịch thành công: Mua {item_name}!", icon="✅")
    else:
        st.toast("Số dư không đủ để thực hiện giao dịch!", icon="❌")

# ==========================================
# 3. THANH ĐIỀU HƯỚNG (SIDEBAR)
# ==========================================
with st.sidebar:
    st.markdown("### ⚡ ED-ODYSSEY")
    st.divider()
    
    # Profile người dùng
    st.markdown("**👦 HUSTLER PROFILE**")
    st.markdown("User: **Explorer_GenZ**")
    st.markdown("Rank: **A (Thợ săn bạc)**")
    st.write("")
    
    # Thẻ Ví tiền chuyên nghiệp
    st.markdown(f"""
        <div class="wallet-card">
            <div class="wallet-title">Ví MoMo / Credit</div>
            <div class="wallet-amount">{st.session_state.balance:,.0f} đ</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Menu điều hướng
    st.markdown("**ĐIỀU HƯỚNG HỆ THỐNG:**")
    menu = st.radio(
        "Menu",
        ["🛒 Blueprint Marketplace", "💻 My Workspace (Đã mua)", "🎯 Bounty Board", "🏛️ Bảo tàng Sai lầm"],
        label_visibility="collapsed"
    )

# ==========================================
# 4. KHU VỰC HIỂN THỊ CHÍNH (MARKETPLACE)
# ==========================================
if menu == "🛒 Blueprint Marketplace":
    # Header
    st.markdown('<div class="market-title">🛒 BLUEPRINT MARKETPLACE</div>', unsafe_allow_html=True)
    st.markdown('<div class="market-subtitle">GIẢI PHÁP THỰC CHIẾN - PAY-AS-YOU-GO</div>', unsafe_allow_html=True)
    st.markdown('<div class="market-desc">Sàn giao dịch ngang hàng (P2P). Thuê Blueprint tương tác chỉ với một ly trà đá.</div>', unsafe_allow_html=True)
    
    # Danh sách sản phẩm
    col1, col2, col3 = st.columns(3)
    
    # Sản phẩm 1
    with col1:
        with st.container(border=True):
            st.subheader("🚀 Ném Xiên 360°")
            st.markdown('<div class="creator-badge">Creator: Hustler_Physics99</div>', unsafe_allow_html=True)
            st.write("Mô phỏng quỹ đạo ném xiên thời gian thực bằng Plotly & NumPy. Phân tích vector vận tốc.")
            st.markdown("**Giá thuê 24h:** :blue[15.000 VNĐ]")
            
            if st.button("Mua bằng MoMo - 15K", key="btn_1", use_container_width=True, type="primary"):
                handle_purchase(15000, "Ném Xiên 360°")

    # Sản phẩm 2
    with col2:
        with st.container(border=True):
            st.subheader("📈 Đồ Thị Động Học")
            st.markdown('<div class="creator-badge">Creator: MathWiz_01</div>', unsafe_allow_html=True)
            st.write("Xử lý dữ liệu vận tốc - thời gian. Tự động tìm cực đại, cực tiểu và phân tích gia tốc.")
            st.markdown("**Giá thuê 24h:** :blue[10.000 VNĐ]")
            
            if st.button("Mua bằng MoMo - 10K", key="btn_2", use_container_width=True, type="primary"):
                handle_purchase(10000, "Đồ Thị Động Học")

    # Sản phẩm 3
    with col3:
        with st.container(border=True):
            st.subheader("🧮 Tool Tích Vô Hướng")
            st.markdown('<div class="creator-badge">Creator: CodeNinja_HN</div>', unsafe_allow_html=True)
            st.write("Thuật toán Python xử lý ma trận và tự động cảnh báo sai sót ký hiệu Vector cho Toán 10.")
            st.markdown("**Giá thuê 24h:** :blue[12.000 VNĐ]")
            
            if st.button("Mua bằng MoMo - 12K", key="btn_3", use_container_width=True, type="primary"):
                handle_purchase(12000, "Tool Tích Vô Hướng")

else:
    # Các trang khác đang xây dựng
    st.info(f"Bạn đang ở khu vực: **{menu}**. Khu vực này đang được nâng cấp!")
