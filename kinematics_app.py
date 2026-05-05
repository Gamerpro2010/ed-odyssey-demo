import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Kinematics Lab | ED-ODYSSEY", layout="wide")

# ==========================================
# CSS CẬP NHẬT: TĂNG ĐỘ TƯƠNG PHẢN MÀU CHỮ
# ==========================================
st.markdown("""
    <style>
    /* Nền sẫm cao cấp */
    .stApp { background-color: #0B0F19; color: #F8FAFC; }

    /* Chỉnh tiêu đề chính rực rỡ hơn */
    .header { 
        font-size: 2.8rem; font-weight: 900; 
        color: #38bdf8;
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
        margin-bottom: 25px; 
    }

    /* Ép màu trắng sáng cho tất cả các nhãn và subheader */
    h1, h2, h3, label, p { color: #f8fafc !important; }

    /* FIX MÀU CHỮ TRONG INFO BOX (Dễ đọc hơn 100%) */
    div[data-testid="stNotification"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid #1e293b !important;
    }
    div[data-testid="stNotification"] p {
        color: #38bdf8 !important; /* Màu xanh sáng */
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }

    /* Tùy chỉnh vùng Upload */
    section[data-testid="stFileUploadDropzone"] {
        background: #111827 !important;
        border: 1px dashed #334155 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">📈 Đồ Thị Động Học V1.1</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("### 📥 Nhập dữ liệu")
    uploaded_file = st.file_uploader("Chọn file CSV thí nghiệm", type=['csv'], key="kinematics_upload")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ Đã nhận file dữ liệu!")
            with st.expander("Xem trước bảng dữ liệu"):
                st.dataframe(df.head(10), use_container_width=True)
        except Exception as e:
            st.error(f"Lỗi đọc file: {e}")

with col2:
    st.markdown("### 📊 Đồ thị phân tích")
    if uploaded_file is not None:
        try:
            cols = df.columns.tolist()
            if len(cols) >= 2:
                x_axis = st.selectbox("Trục hoành (Thời gian):", cols, index=0)
                y_axis = st.selectbox("Trục tung (Vận tốc/Quãng đường):", cols, index=1)
                
                fig = px.line(df, x=x_axis, y=y_axis, markers=True, template="plotly_dark")
                fig.update_traces(line_color='#38bdf8', line_width=3)
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(gridcolor='#1e293b'),
                    yaxis=dict(gridcolor='#1e293b')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠️ File CSV cần ít nhất 2 cột để vẽ đồ thị!")
        except Exception as e:
            st.error(f"Lỗi hiển thị đồ thị: {e}")
    else:
        # Hộp thông báo với màu chữ đã được fix
        st.info("Hệ thống sẵn sàng. Hãy tải file lên ở cột bên trái để bắt đầu phân tích.")
