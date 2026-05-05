import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Kinematics Lab", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0B0F19; color: #F8FAFC; }
    .header { font-size: 2.2rem; font-weight: 800; color: #38BDF8; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">📈 Đồ Thị Động Học V1.1</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("📥 Nhập dữ liệu")
    uploaded_file = st.file_uploader("Chọn file CSV thí nghiệm", type=['csv'], key="kinematics_upload")
    
    if uploaded_file is not None:
        # Đọc dữ liệu ngay lập tức
        df = pd.read_csv(uploaded_file)
        st.write("📋 Xem trước dữ liệu:")
        st.dataframe(df.head(5), use_container_width=True)

with col2:
    st.subheader("📊 Đồ thị phân tích")
    if uploaded_file is not None:
        try:
            # Tự động tìm cột phù hợp
            cols = df.columns.tolist()
            x_axis = st.selectbox("Trục hoành (Thời gian):", cols, index=0)
            y_axis = st.selectbox("Trục tung (Vận tốc/Quãng đường):", cols, index=1 if len(cols)>1 else 0)
            
            fig = px.line(df, x=x_axis, y=y_axis, markers=True, template="plotly_dark")
            fig.update_traces(line_color='#38bdf8')
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Lỗi hiển thị: {e}")
    else:
        st.info("Hệ thống sẵn sàng. Hãy tải file lên ở cột bên trái.")
