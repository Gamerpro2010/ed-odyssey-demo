import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Kinematics Lab", layout="wide")

# Giao diện đồng bộ với ED-ODYSSEY
st.markdown("""
    <style>
    .stApp { background-color: #0B0F19; color: #F8FAFC; }
    .header { font-size: 2.2rem; font-weight: 800; color: #38BDF8; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">📈 Đồ Thị Động Học V1.0</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("📥 Nhập dữ liệu")
    uploaded_file = st.file_uploader("Tải file thí nghiệm (.csv)", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Tải file thành công!")

with col2:
    st.subheader("📊 Kết quả phân tích")
    if uploaded_file:
        # Giả sử file có cột 'time' và 'velocity'
        fig = px.line(df, x='time', y='velocity', title='Đồ thị Vận tốc - Thời gian')
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Đang chờ dữ liệu đầu vào...")
