import streamlit as st
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components
import time

# ==========================================
# 1. CẤU HÌNH TRANG & CSS (CHUẨN SAAS/EDTECH)
# ==========================================
st.set_page_config(page_title="ED-ODYSSEY | Workspace", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    /* Làm gọn không gian tổng thể */
    .block-container { padding-top: 2rem; max-width: 1100px; }
    
    /* Box hiển thị số dư Credit (Sang trọng, tối giản) */
    .wallet-box {
        padding: 15px; 
        border-radius: 8px; 
        background-color: #1e293b; 
        border: 1px solid #334155; 
        text-align: center; 
        margin-bottom: 20px;
    }
    .wallet-label { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; color: #94a3b8; }
    .wallet-value { font-size: 2rem; font-weight: 700; color: #38bdf8; }
    
    /* Thiết kế thẻ Marketplace */
    .course-card {
        padding: 20px;
        border-radius: 8px;
        background-color: #0f172a;
        border: 1px solid #1e293b;
        transition: all 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .course-card:hover { border-color: #38bdf8; }
    .course-title { font-size: 1.1rem; font-weight: 700; margin-bottom: 5px; color: #f8fafc; }
    .course-author { font-size: 0.8rem; color: #64748b; margin-bottom: 12px; }
    .course-desc { font-size: 0.9rem; color: #94a3b8; margin-bottom: 20px; line-height: 1.4; }
    .course-price { font-size: 1.2rem; font-weight: 700; color: #38bdf8; margin-bottom: 15px; }
    
    /* Module Workspace (Thay thế các hộp xanh nhàm chán) */
    .module-box {
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #334155;
        background-color: #1e293b;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. KHỞI TẠO STATE (Đơn vị nhỏ gọn: 50 CR)
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
        st.toast(f"Đã mở khóa: {tool_name}", icon="✅")
    else:
        st.error("Số dư Credit không đủ. Vui lòng nạp thêm.")

# ==========================================
# 3. SIDEBAR (DASHBOARD CHUYÊN NGHIỆP)
# ==========================================
with st.sidebar:
    st.markdown("### 🎓 ED-ODYSSEY")
    st.caption("Workspace & Marketplace")
    st.write("---")
    
    # Hiển thị số dư nhỏ gọn, bỏ phần nghìn
    st.markdown(f"""
        <div class="wallet-box">
            <div class="wallet-label">Số dư Credit</div>
            <div class="wallet-value">{st.session_state.credit_balance} CR</div>
        </div>
    """, unsafe_allow_html=True)
    
    # LOGIC NẠP TIỀN THỰC TẾ
    with st.popover("➕ Nạp Credit", use_container_width=True):
        st.markdown("**Quy đổi: 1.000 VNĐ = 1 CR**")
        method = st.selectbox("Kênh thanh toán", ["Ví MoMo", "VietQR (Ngân hàng)"])
        amount = st.number_input("Số lượng Credit muốn nạp", min_value=10, step=10, value=20)
        
        st.info(f"Vui lòng chuyển {amount * 1000:,} VNĐ qua {method} với nội dung: NẠP.")
        
        # Bắt buộc xác nhận mới hiện nút nạp (Chống cộng tiền ảo)
        if st.checkbox("Tôi xác nhận đã chuyển tiền thật"):
            if st.button("Hoàn tất giao dịch", type="primary", use_container_width=True):
                with st.spinner("Đang đối soát giao dịch..."):
                    time.sleep(1) # Giả lập thời gian server kiểm tra ngân hàng
                    st.session_state.credit_balance += amount
                    st.rerun()

    st.write("---")
    menu = st.radio("ĐIỀU HƯỚNG", ["📦 Marketplace", "💻 My Workspace", "🎯 Bounty Board"], label_visibility="collapsed")

# ==========================================
# 4. KHU VỰC CHÍNH (MAIN CONTENT)
# ==========================================

if menu == "📦 Marketplace":
    st.markdown('<h2>Blueprint Marketplace</h2>', unsafe_allow_html=True)
    st.write("Trao đổi các công cụ hỗ trợ học tập thực chiến (Pay-as-you-go).")
    st.write("")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"""
            <div class="course-card">
                <div>
                    <div class="course-title">Mô Phỏng Vật Lý 10</div>
                    <div class="course-author">🏢 Nền tảng ED-ODYSSEY</div>
                    <div class="course-desc">Môi trường giả lập tương tác chuyên sâu. Phân tích vector và động học thời gian thực.</div>
                </div>
                <div class="course-price">15 CR</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mua bằng Credit", key="b1", use_container_width=True):
            process_purchase("Mô Phỏng Vật Lý 10", 15)

    with c2:
        st.markdown(f"""
            <div class="course-card">
                <div>
                    <div class="course-title">Đồ Thị Động Học</div>
                    <div class="course-author">👤 MathWiz_01</div>
                    <div class="course-desc">Hệ thống xử lý dữ liệu vận tốc - thời gian. Tự động tìm cực đại, cực tiểu và gia tốc.</div>
                </div>
                <div class="course-price">10 CR</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mua bằng Credit", key="b2", use_container_width=True):
            process_purchase("Đồ Thị Động Học", 10)

    with c3:
        st.markdown(f"""
            <div class="course-card">
                <div>
                    <div class="course-title">Xử Lý Tích Vô Hướng</div>
                    <div class="course-author">👤 CodeNinja_HN</div>
                    <div class="course-desc">Thuật toán xử lý ma trận và cảnh báo sai sót ký hiệu Vector cho môn Toán hình học 10.</div>
                </div>
                <div class="course-price">12 CR</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mua bằng Credit", key="b3", use_container_width=True):
            process_purchase("Xử Lý Tích Vô Hướng", 12)

elif menu == "💻 My Workspace":
    st.markdown('<h2>My Workspace</h2>', unsafe_allow_html=True)
    st.write("Không gian làm việc và chạy các ứng dụng bạn đã sở hữu.")
    st.divider()
    
    if not st.session_state.owned_tools:
        st.info("Workspace trống. Hãy ghé Marketplace để trang bị công cụ.")
    else:
        # Nhúng Iframe web Vật Lý 10
        if "Mô Phỏng Vật Lý 10" in st.session_state.owned_tools:
            st.markdown("### 🚀 Mô Phỏng Vật Lý 10")
            components.iframe("https://mo-phong-vat-ly-10.streamlit.app/?embed=true", height=700, scrolling=True)
            st.write("---")
            
        # Thiết kế lại UI giả lập thay cho hộp xanh trống rỗng
        if "Đồ Thị Động Học" in st.session_state.owned_tools:
            st.markdown('<div class="module-box">', unsafe_allow_html=True)
            st.markdown("#### 📈 Module Phân Tích Đồ Thị Động Học")
            st.write("Công cụ đang chờ nạp dữ liệu đầu vào để bắt đầu quá trình phân tích.")
            st.file_uploader("Tải lên file dữ liệu (.csv, .xlsx) của bạn", type=['csv', 'xlsx'])
            st.button("Bắt đầu trích xuất đồ thị", disabled=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Thiết kế lại UI giả lập cho Tích vô hướng
        if "Xử Lý Tích Vô Hướng" in st.session_state.owned_tools:
            st.markdown('<div class="module-box">', unsafe_allow_html=True)
            st.markdown("#### 🧮 Engine Tích Vô Hướng")
            col_a, col_b = st.columns(2)
            col_a.text_input("Nhập toạ độ Vector A (Ví dụ: 2, -3):")
            col_b.text_input("Nhập toạ độ Vector B (Ví dụ: 1, 5):")
            st.button("Khởi chạy tính toán", type="primary")
            st.markdown('</div>', unsafe_allow_html=True)

elif menu == "🎯 Bounty Board":
    st.markdown('<h2>Bounty Board</h2>', unsafe_allow_html=True)
    st.info("Đang bảo trì và cập nhật hệ thống nhiệm vụ mới.")
