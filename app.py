import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 1. CẤU HÌNH TRANG - PHONG CÁCH TỐI GIẢN
# ==========================================
st.set_page_config(
    page_title="ED-ODYSSEY | Workspace",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS nhỏ để chỉnh lại font và khoảng cách cho thanh lịch
st.markdown("""
    <style>
    .st-emotion-cache-16txtl3 { padding-top: 2rem; }
    .creator-text { font-size: 0.85rem; color: #888; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. KHỞI TẠO HỆ THỐNG DỮ LIỆU
# ==========================================
if 'credit_balance' not in st.session_state:
    st.session_state.credit_balance = 50000  # Đơn vị là Credit
if 'owned_tools' not in st.session_state:
    st.session_state.owned_tools = []

def buy_tool(tool_name, price):
    if tool_name in st.session_state.owned_tools:
        st.toast(f"Bạn đã sở hữu {tool_name} rồi!", icon="ℹ️")
    elif st.session_state.credit_balance >= price:
        st.session_state.credit_balance -= price
        st.session_state.owned_tools.append(tool_name)
        st.toast(f"Giao dịch thành công! Đã thêm {tool_name} vào Workspace.", icon="🎉")
    else:
        st.error("Số dư Credit không đủ. Vui lòng nạp thêm!")

# ==========================================
# 3. THANH ĐIỀU HƯỚNG (SIDEBAR) CHUYÊN NGHIỆP
# ==========================================
with st.sidebar:
    st.title("⚡ ED-ODYSSEY")
    
    # Profile gọn gàng
    st.markdown("**👦 Explorer_GenZ**")
    st.caption("Hạng: Thợ săn bạc")
    st.write("---")
    
    # Khu vực Ví Credit (Đã sửa theo đúng logic của ông)
    with st.container(border=True):
        st.metric(label="Số dư Credit", value=f"{st.session_state.credit_balance:,.0f} CR")
        
        # Nút nạp tiền bằng MoMo được đặt đúng chỗ
        with st.popover("💳 Nạp thêm Credit"):
            st.markdown("Chọn phương thức thanh toán:")
            method = st.selectbox("Cổng thanh toán", ["Ví MoMo", "ZaloPay", "Chuyển khoản Ngân hàng"], label_visibility="collapsed")
            st.button(f"Xác nhận nạp qua {method}", use_container_width=True, type="primary")
    
    st.write("---")
    st.markdown("**ĐIỀU HƯỚNG:**")
    menu = st.radio(
        "Navigation",
        ["🛒 Blueprint Marketplace", "💻 My Workspace", "🎯 Bounty Board"],
        label_visibility="collapsed"
    )

# ==========================================
# 4. KHU VỰC CHÍNH
# ==========================================

if menu == "🛒 Blueprint Marketplace":
    st.header("🛒 Blueprint Marketplace")
    st.write("Khám phá và trang bị các công cụ học tập thực chiến.")
    st.write("") # Tạo khoảng trống
    
    col1, col2, col3 = st.columns(3)
    
    # Thiết kế Thẻ sản phẩm (Card) thân thiện
    with col1.container(border=True):
        st.markdown("### 🚀 Ném Xiên 360°")
        st.markdown('<p class="creator-text">Cung cấp bởi: Hustler_Physics99</p>', unsafe_allow_html=True)
        st.write("Mô phỏng quỹ đạo ném xiên thời gian thực. Phân tích vector vận tốc và tầm xa.")
        st.markdown("**Giá: 15,000 CR**")
        if st.button("Mua bằng Credit", key="btn1", use_container_width=True, type="primary"):
            buy_tool("Ném Xiên 360°", 15000)

    with col2.container(border=True):
        st.markdown("### 📈 Đồ Thị Động Học")
        st.markdown('<p class="creator-text">Cung cấp bởi: MathWiz_01</p>', unsafe_allow_html=True)
        st.write("Xử lý dữ liệu vận tốc - thời gian. Tự động tìm cực đại, cực tiểu và gia tốc.")
        st.markdown("**Giá: 10,000 CR**")
        if st.button("Mua bằng Credit", key="btn2", use_container_width=True, type="primary"):
            buy_tool("Đồ Thị Động Học", 10000)

    with col3.container(border=True):
        st.markdown("### 🧮 Tích Vô Hướng")
        st.markdown('<p class="creator-text">Cung cấp bởi: CodeNinja_HN</p>', unsafe_allow_html=True)
        st.write("Thuật toán xử lý ma trận và tự động cảnh báo sai sót ký hiệu Vector cho Toán 10.")
        st.markdown("**Giá: 12,000 CR**")
        if st.button("Mua bằng Credit", key="btn3", use_container_width=True, type="primary"):
            buy_tool("Tool Tích Vô Hướng", 12000)

elif menu == "💻 My Workspace":
    st.header("💻 Không gian làm việc (My Workspace)")
    st.write("Các công cụ bạn đã sở hữu sẽ xuất hiện tại đây.")
    st.divider()
    
    if not st.session_state.owned_tools:
        st.info("Bàn làm việc của bạn đang trống. Hãy vào Marketplace để trang bị thêm công cụ nhé!")
    else:
        # Nếu đã mua Ném xiên, hiển thị công cụ thật
        if "Ném Xiên 360°" in st.session_state.owned_tools:
            with st.expander("🚀 Khởi chạy: Ném Xiên 360°", expanded=True):
                st.write("Nhập thông số để mô phỏng quỹ đạo:")
                c1, c2 = st.columns(2)
                v0 = c1.slider("Vận tốc ban đầu (m/s)", 10, 80, 40)
                angle = c2.slider("Góc ném (độ)", 10, 80, 45)
                
                # Biểu diễn đồ thị
                g = 9.8
                theta = np.radians(angle)
                t_flight = (2 * v0 * np.sin(theta)) / g
                t = np.linspace(0, t_flight, 100)
                x = v0 * np.cos(theta) * t
                y = v0 * np.sin(theta) * t - 0.5 * g * t**2
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(width=3, color='#3b82f6')))
                fig.update_layout(title="Mô phỏng Quỹ đạo", xaxis_title="Tầm xa (m)", yaxis_title="Độ cao (m)", margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig, use_container_width=True)
                
        if "Đồ Thị Động Học" in st.session_state.owned_tools:
            with st.expander("📈 Khởi chạy: Đồ Thị Động Học"):
                st.success("Module này đã được kích hoạt và đang chờ cập nhật dữ liệu đầu vào.")
                
        if "Tool Tích Vô Hướng" in st.session_state.owned_tools:
            with st.expander("🧮 Khởi chạy: Tool Tích Vô Hướng"):
                st.success("Module thuật toán đã sẵn sàng.")

elif menu == "🎯 Bounty Board":
    st.header("🎯 Bounty Board")
    st.info("Khu vực săn tiền thưởng đang được nâng cấp. Quay lại sau nhé!")
