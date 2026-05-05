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

st.markdown('<div class="header">📈 Đồ Thị Động Học V1.0</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("📥 Nhập dữ liệu")
    uploaded_file = st.file_uploader("Tải file thí nghiệm (.csv)", type=['csv'])

with col2:
    st.subheader("📊 Kết quả phân tích")
    if uploaded_file is not None:
        try:
            # Đọc dữ liệu
            df = pd.read_csv(uploaded_file)
            
            # Kiểm tra nếu file có dữ liệu
            if not df.empty:
                # Tự động lấy 2 cột đầu tiên nếu không tìm thấy tên 'time'/'velocity'
                x_col = 'time' if 'time' in df.columns else df.columns[0]
                y_col = 'velocity' if 'velocity' in df.columns else df.columns[1]
                
                fig = px.line(df, x=x_col, y=y_col, 
                             title=f'Đồ thị {y_col} theo {x_col}',
                             template="plotly_dark",
                             line_shape="spline")
                fig.update_traces(line_color='#38bdf8', line_width=3)
                st.plotly_chart(fig, use_container_width=True)
                
                # Tính toán nhanh
                delta_v = df[y_col].iloc[-1] - df[y_col].iloc[0]
                delta_t = df[x_col].iloc[-1] - df[x_col].iloc[0]
                st.success(f"Phân tích hoàn tất! Gia tốc ước tính: {delta_v/delta_t:.2f} m/s²")
        except Exception as e:
            st.error(f"Lỗi cấu trúc file: {e}")
    else:
        st.info("Hệ thống đang đợi file .csv từ ông...")
