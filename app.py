import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# ==========================================
# 1. CẤU HÌNH TRANG & GIAO DIỆN (UI/UX)
# Đạt chuẩn "Dark Mode" & "Hacker Command Center" cho Gen Z
# ==========================================
st.set_page_config(page_title="ED-ODYSSEY | P2P STEM Marketplace", page_icon="🚀", layout="wide")

# Custom CSS cho phong cách Cyberpunk/Dark Mode
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #00FF41;
        font-family: 'Courier New', Courier, monospace;
    }
    .metric-card {
        background-color: #1E1E1E;
        border: 1px solid #00FF41;
        padding: 15px;
        border-radius: 5px;
        text-align: center;
    }
    h1, h2, h3 { color: #00FF41 !important; text-transform: uppercase; }
    .stButton>button {
        width: 100%;
        background-color: #00FF41;
        color: #000000;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #000000;
        color: #00FF41;
        border: 1px solid #00FF41;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. QUẢN LÝ TRẠNG THÁI (SESSION STATE)
# Giả lập Database & Thanh toán vi mô (MoMo)
# ==========================================
if 'user_balance' not in st.session_state:
    st.session_state.user_balance = 50000  # Tặng sẵn 50.000 VNĐ để test
if 'purchased_blueprints' not in st.session_state:
    st.session_state.purchased_blueprints = []
if 'current_view' not in st.session_state:
    st.session_state.current_view = "Marketplace"

def buy_item(item_name, price):
    if item_name in st.session_state.purchased_blueprints:
        st.warning("Bạn đã sở hữu Blueprint này!")
    elif st.session_state.user_balance >= price:
        # Giả lập độ trễ gọi API MoMo Zero-friction
        with st.spinner("Đang xử lý thanh toán qua API MoMo..."):
            time.sleep(1)
        st.session_state.user_balance -= price
        st.session_state.purchased_blueprints.append(item_name)
        st.success(f"Thanh toán thành công {price:,.0f} VNĐ! Blueprint đã được mở khóa.")
    else:
        st.error("Số dư không đủ. Vui lòng nạp thêm qua MoMo!")

# ==========================================
# 3. SIDEBAR - HỒ SƠ HUSTLER & ĐIỀU HƯỚNG
# ==========================================
with st.sidebar:
    st.title("⚡ ED-ODYSSEY")
    st.markdown("---")
    st.markdown("### 🧑‍💻 HUSTLER PROFILE")
    st.markdown("**User:** Explorer_GenZ")
    st.markdown("**Rank:** A (Thợ săn bạc)")
    
    # Hiển thị số dư
    st.markdown(f"<div class='metric-card'><h3>Ví MoMo / Credit</h3><h2>{st.session_state.user_balance:,.0f} ₫</h2></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Menu điều hướng
    menu = ["🛒 Blueprint Marketplace", "💻 My Workspace (Đã mua)", "🎯 Bounty Board", "🏛️ Bảo tàng Sai lầm"]
    choice = st.radio("ĐIỀU HƯỚNG HỆ THỐNG:", menu)

# ==========================================
# 4. GIAO DIỆN CHÍNH (MAIN VIEW)
# ==========================================

# --- VIEW 1: BLUEPRINT MARKETPLACE ---
if choice == "🛒 Blueprint Marketplace":
    st.title("🛒 Blueprint Marketplace")
    st.subheader("Giải pháp Thực chiến - Pay-as-you-go")
    st.write("Sàn giao dịch ngang hàng (P2P). Thuê Blueprint tương tác chỉ với một ly trà đá.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("### 🚀 Ném xiên 360°")
        st.write("**Creator:** Hustler_Physics99")
        st.write("Mô phỏng quỹ đạo ném xiên thời gian thực bằng Plotly & NumPy. Phân tích vector vận tốc.")
        st.write("**Giá thuê 24h: 15.000 VNĐ**")
        if st.button("Mua bằng MoMo - 15K", key="buy_1"):
            buy_item("Projectile Motion", 15000)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("### 📈 Đồ thị Động học")
        st.write("**Creator:** MathWiz_01")
        st.write("Xử lý dữ liệu vận tốc - thời gian. Tìm cực đại, cực tiểu tự động.")
        st.write("**Giá thuê 24h: 10.000 VNĐ**")
        if st.button("Mua bằng MoMo - 10K", key="buy_2"):
            buy_item("Kinematics Graph", 10000)
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("### 🧮 Tool Tích Vô Hướng")
        st.write("**Creator:** CodeNinja_HN")
        st.write("Thuật toán Python xử lý ma trận và cảnh báo sai sót ký hiệu Vector.")
        st.write("**Giá thuê 24h: 12.000 VNĐ**")
        if st.button("Mua bằng MoMo - 12K", key="buy_3"):
            buy_item("Vector Matrix", 12000)
        st.markdown("</div>", unsafe_allow_html=True)

# --- VIEW 2: MY WORKSPACE (Trải nghiệm tương tác STEM) ---
elif choice == "💻 My Workspace (Đã mua)":
    st.title("💻 My Workspace")
    st.write("Không gian tương tác thực chiến của bạn.")
    
    if len(st.session_state.purchased_blueprints) == 0:
        st.info("Bạn chưa sở hữu Blueprint nào. Hãy quay lại Marketplace để nạp vũ khí!")
    
    if "Projectile Motion" in st.session_state.purchased_blueprints:
        st.markdown("---")
        st.subheader("🚀 MODULE: MÔ PHỎNG QUỸ ĐẠO NÉM XIÊN (Interactive Blueprint)")
        st.write("Sử dụng lõi tính toán **NumPy** và engine render đồ thị **Plotly**.")
        
        # UI Tương tác cho học sinh
        c1, c2, c3 = st.columns(3)
        v0 = c1.slider("Vận tốc ban đầu (v0) [m/s]", 10, 100, 50)
        angle = c2.slider("Góc ném (θ) [Độ]", 10, 90, 45)
        g = c3.slider("Gia tốc trọng trường (g) [m/s²]", 9.0, 10.0, 9.8)
        
        # Xử lý Toán học bằng NumPy (C-level execution)
        theta_rad = np.radians(angle)
        t_flight = 2 * v0 * np.sin(theta_rad) / g
        t = np.linspace(0, t_flight, num=200)
        
        # Phương trình chuyển động
        x = v0 * np.cos(theta_rad) * t
        y = v0 * np.sin(theta_rad) * t - 0.5 * g * t**2
        
        max_height = (v0**2 * (np.sin(theta_rad)**2)) / (2 * g)
        max_distance = x[-1]
        
        # Trực quan hóa dữ liệu bằng Plotly (Dynamic Data Visualization)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Quỹ đạo', line=dict(color='#00FF41', width=3)))
        fig.add_trace(go.Scatter(x=[x[np.argmax(y)]], y=[max_height], mode='markers', name='Đỉnh', marker=dict(color='red', size=10)))
        
        fig.update_layout(
            title="Đồ thị Động học 2D",
            xaxis_title="Trục X - Độ dịch chuyển (m)",
            yaxis_title="Trục Y - Độ cao (m)",
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.success(f"**Kết quả tính toán:** Tầm xa tối đa: {max_distance:.2f} m | Độ cao tối đa: {max_height:.2f} m")

# --- VIEW 3: BOUNTY BOARD ---
elif choice == "🎯 Bounty Board":
    st.title("🎯 Bảng Săn Tiền Thưởng (Bounty Board)")
    st.write("Nơi Hustler kiếm tiền từ chất xám. Viết Code/Tool để giải quyết vấn đề của Explorer.")
    
    bounties = [
        {"Task": "Thuật toán tối ưu hóa diện tích bề mặt khối đa diện", "Rank": "S", "Reward": "1,000,000 VNĐ", "Status": "Open"},
        {"Task": "Mô phỏng lực ma sát mặt phẳng nghiêng (Có slider chỉnh hệ số)", "Rank": "A", "Reward": "150,000 VNĐ", "Status": "In Progress"},
        {"Task": "Tool tự động tính phương sai, tứ phân vị từ file Excel", "Rank": "B", "Reward": "50,000 VNĐ", "Status": "Open"}
    ]
    st.table(bounties)
    st.button("🔥 Nhận Nhiệm Vụ (Submit Code)")

# --- VIEW 4: BẢO TÀNG SAI LẦM ---
elif choice == "🏛️ Bảo tàng Sai lầm":
    st.title("🏛️ The Mistake Museum")
    st.write("Thương mại hóa sự thất bại. Học từ những lỗi sai kinh điển (Case studies).")
    
    st.error("💀 LỖI #404: Nhầm lẫn dấu Vector trong Tích Vô Hướng (Hình học 10)")
    st.write("Người mắc lỗi: Explorer_Huy (Đã bị trừ tiền Ký quỹ - Escrow)")
    st.write("Bài học: Phân tích lại hàm `np.dot()` trong Python...")
    st.button("Mua Blueprint rút kinh nghiệm - 5.000 VNĐ")
