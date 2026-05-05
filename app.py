import streamlit as st
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components
import time

# ==========================================
# 1. CẤU HÌNH TRANG & CSS (UI/UX CHUẨN EDTECH)
# ==========================================
st.set_page_config(page_title="ED-ODYSSEY", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    /* Ép sát lề trên để giao diện thoáng hơn */
    .block-container { padding-top: 1.5rem; max-width: 1200px; }
    
    /* Box Ví Credit trên Sidebar */
    .wallet-box {
        padding: 15px; 
        border-radius: 12px; 
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155; 
        text-align: center; 
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .wallet-label { font-size: 0.75rem; text-transform: uppercase; font-weight: 600; color: #94a3b8; margin-bottom: 5px;}
    .wallet-value { font-size: 2.2rem; font-weight: 800; color: #38bdf8; line-height: 1; }
    
    /* Thiết kế Thumbnail (Ảnh bìa) cho Sản phẩm */
    .thumb-1 { height: 120px; border-radius: 8px; background: linear-gradient(135deg, #f6d365 0%, #fda085 100%); margin-bottom: 15px; }
    .thumb-2 { height: 120px; border-radius: 8px; background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); margin-bottom: 15px; }
    .thumb-3 { height: 120px; border-radius: 8px; background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%); margin-bottom: 15px; }
    
    /* Typography Sản phẩm */
    .p-title { font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin-bottom: 5px; }
    .p-author { font-size: 0.8rem; color: #64748b; margin-bottom: 10px; }
    .p-desc { font-size: 0.9rem; color: #cbd5e1; line-height: 1.5; margin-bottom: 15px; height: 65px; overflow: hidden; }
    .p-price { font-size: 1.3rem; font-weight: 800; color: #38bdf8; margin-bottom: 15px; }
    
    /* Tùy chỉnh Tab của Streamlit cho đẹp hơn */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { padding-top: 10px; padding-bottom: 10px; border-radius: 5px 5px 0 0; }
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
    else:
        st.error("Số dư Credit không đủ!")

# ==========================================
# 3. SIDEBAR (BỐ CỤC DASHBOARD)
# ==========================================
with st.sidebar:
    st.markdown("## 🚀 ED-ODYSSEY")
    st.write("---")
    
    st.markdown(f"""
        <div class="wallet-box">
            <div class="wallet-label">Số dư Credit</div>
            <div class="wallet-value">{st.session_state.credit_balance} CR</div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.popover("💳 Nạp Credit", use_container_width=True):
        st.markdown("**Tỷ giá: 1.000 VNĐ = 1 CR**")
        method = st.selectbox("Phương thức", ["Ví MoMo", "Chuyển khoản"])
        amount = st.number_input("Số CR muốn nạp", min_value=10, step=10, value=20)
        st.info(f"Vui lòng thanh toán {amount * 1000:,} VNĐ.")
        if st.checkbox("Xác nhận đã chuyển tiền"):
            if st.button("Hoàn tất", type="primary", use_container_width=True):
                with st.spinner("Đang xử lý..."):
                    time.sleep(1)
                    st.session_state.credit_balance += amount
                    st.rerun()

    st.write("---")
    menu = st.radio("ĐIỀU HƯỚNG", ["🛒 Blueprint Marketplace", "💻 My Workspace", "🎯 Bounty Board"], label_visibility="collapsed")

# ==========================================
# 4. KHU VỰC CHÍNH (MAIN LAYOUT)
# ==========================================

if menu == "🛒 Blueprint Marketplace":
    st.title("Blueprint Marketplace")
    st.markdown("Trang bị các công cụ hỗ trợ học tập thực chiến (Pay-as-you-go).")
    st.write("")
    
    # Bố cục Grid 3 cột cho thẻ sản phẩm
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1.container(border=True):
        st.markdown('<div class="thumb-1"></div>', unsafe_allow_html=True) # Ảnh bìa
        st.markdown('<div class="p-title">Mô Phỏng Vật Lý 10</div>', unsafe_allow_html=True)
        st.markdown('<div class="p-author">Creator: ED-ODYSSEY</div>', unsafe_allow_html=True)
        st.markdown('<div class="p-desc">Môi trường giả lập tương tác chuyên sâu. Phân tích vector và động học thời gian thực.</div>', unsafe_allow_html=True)
        st.markdown('<div class="p-price">15 CR</div>', unsafe_allow_html=True)
        if st.button("Mua ngay", key="b1", use_container_width=True, type="primary"):
            process_purchase("Mô Phỏng Vật Lý 10", 15)

    with col2.container(border=True):
        st.markdown('<div class="thumb-2"></div>', unsafe_allow_html=True)
        st.markdown('<div class="p-title">Đồ Thị Động Học</div>', unsafe_allow_html=True)
        st.markdown('<div class="p-author">Creator: MathWiz_01</div>', unsafe_allow_html=True)
        st.markdown('<div class="p-desc">Xử lý dữ liệu vận tốc - thời gian. Tự động tìm cực đại, cực tiểu và gia tốc nhanh chóng.</div>', unsafe_allow_html=True)
        st.markdown('<div class="p-price">10 CR</div>', unsafe_allow_html=True)
        if st.button("Mua ngay", key="b2", use_container_width=True, type="primary"):
            process_purchase("Đồ Thị Động Học", 10)

    with col3.container(border=True):
        st.markdown('<div class="thumb-3"></div>', unsafe_allow_html=True)
        st.markdown('<div class="p-title">Xử Lý Tích Vô Hướng</div>', unsafe_allow_html=True)
        st.markdown('<div class="p-author">Creator: CodeNinja_HN</div>', unsafe_allow_html=True)
        st.markdown('<div class="p-desc">Thuật toán xử lý ma trận và cảnh báo sai sót ký hiệu Vector cho môn Toán hình học 10.</div>', unsafe_allow_html=True)
        st.markdown('<div class="p-price">12 CR</div>', unsafe_allow_html=True)
        if st.button("Mua ngay", key="b3", use_container_width=True, type="primary"):
            process_purchase("Xử Lý Tích Vô Hướng", 12)

elif menu == "💻 My Workspace":
    st.title("My Workspace")
    st.markdown("Bàn làm việc kỹ thuật số của bạn.")
    st.write("")
    
    if not st.session_state.owned_tools:
        st.info("Workspace của bạn đang trống. Hãy vào Marketplace để mua công cụ nhé.")
    else:
        # BỐ CỤC TAB ĐỘNG (Infinitely better layout)
        tabs = st.tabs(st.session_state.owned_tools)
        
        for i, tool in enumerate(st.session_state.owned_tools):
            with tabs[i]:
                st.write("") # Padding
                
                if tool == "Mô Phỏng Vật Lý 10":
                    components.iframe("https://mo-phong-vat-ly-10.streamlit.app/?embed=true", height=700, scrolling=True)
                    
                elif tool == "Đồ Thị Động Học":
                    # Bố cục chia cột (Split Screen Layout) chuẩn phần mềm
                    left, right = st.columns([1, 2], gap="large")
                    with left:
                        st.subheader("📥 Dữ liệu đầu vào")
                        st.file_uploader("Tải file (.csv, .xlsx)", type=['csv', 'xlsx'])
                        st.button("Phân tích dữ liệu", type="primary", disabled=True)
                    with right:
                        st.subheader("📊 Kết quả phân tích")
                        st.info("Biểu đồ và các điểm cực trị sẽ xuất hiện tại đây sau khi bạn nạp dữ liệu thành công.")
                        
                elif tool == "Xử Lý Tích Vô Hướng":
                    left, right = st.columns([1, 1], gap="large")
                    with left:
                        st.subheader("🧮 Nhập Toạ Độ")
                        st.text_input("Vector A (x, y):", placeholder="Ví dụ: 2, -3")
                        st.text_input("Vector B (x, y):", placeholder="Ví dụ: 1, 5")
                        st.button("Tính toán", type="primary")
                    with right:
                        st.subheader("💡 Kết Quả")
                        st.success("Hệ thống đã sẵn sàng tính Tích vô hướng, Độ dài và Góc giữa 2 Vector.")

elif menu == "🎯 Bounty Board":
    st.title("Bounty Board")
    st.info("Hệ thống nhiệm vụ đang được cập nhật.")
