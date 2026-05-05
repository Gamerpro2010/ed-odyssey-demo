import streamlit as st
import numpy as np

st.set_page_config(page_title="Vector Engine | ED-ODYSSEY", layout="wide")

st.markdown("""
    <style>
    /* Nền lưới tọa độ */
    .stApp {
        background-color: #0B0F19;
        background-image: 
            linear-gradient(rgba(56, 189, 248, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(56, 189, 248, 0.05) 1px, transparent 1px);
        background-size: 30px 30px;
    }

    /* Đổi phông chữ và ép màu trắng cho tất cả nhãn (Labels) */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="st-"], label {
        font-family: 'JetBrains+Mono', monospace !important;
        color: #f8fafc !important; /* Ép chữ trắng cho toàn bộ nhãn */
    }

    .vector-header {
        font-size: 2.5rem; font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 25px;
    }

    /* Card nhập liệu */
    .input-card {
        background: rgba(17, 24, 39, 0.9);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 25px;
        backdrop-filter: blur(10px);
    }

    /* Hộp kết quả tùy chỉnh (High Contrast) */
    .result-box {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        font-weight: 700;
        border: 1px solid;
    }
    .res-sum { background: rgba(34, 197, 94, 0.1); border-color: #22c55e; color: #4ade80 !important; }
    .res-diff { background: rgba(56, 189, 248, 0.1); border-color: #38bdf8; color: #7dd3fc !important; }

    /* Nút bấm Gradient xanh */
    div.stButton > button {
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%) !important;
        border: none !important; color: white !important;
        font-weight: 800 !important; border-radius: 8px !important;
        padding: 12px !important; transition: 0.3s;
    }
    div.stButton > button:hover { transform: scale(1.01); filter: brightness(1.1); }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="vector-header">🧮 Vector Coordinate Engine</div>', unsafe_allow_html=True)

with st.container():
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.subheader("Vector $\\vec{u}$")
        ux = st.number_input("Hoành độ x(u):", value=2.0, step=0.5, format="%.2f")
        uy = st.number_input("Tung độ y(u):", value=3.0, step=0.5, format="%.2f")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.subheader("Vector $\\vec{v}$")
        vx = st.number_input("Hoành độ x(v):", value=1.0, step=0.5, format="%.2f")
        vy = st.number_input("Tung độ y(v):", value=-2.0, step=0.5, format="%.2f")
        st.markdown('</div>', unsafe_allow_html=True)

st.write("")
if st.button("🚀 Thực thi phép toán Vector", use_container_width=True):
    u = np.array([ux, uy])
    v = np.array([vx, vy])
    
    vec_sum = u + v
    vec_diff = u - v
    dot_product = np.dot(u, v)
    mag_u = np.linalg.norm(u)
    mag_v = np.linalg.norm(v)

    st.write("")
    
    # Hiển thị kết quả tọa độ với hộp tùy chỉnh
    res_a, res_b = st.columns(2)
    with res_a:
        st.markdown(f'<div class="result-box res-sum">Tổng u + v: ({vec_sum[0]:.1f} ; {vec_sum[1]:.1f})</div>', unsafe_allow_html=True)
    with res_b:
        st.markdown(f'<div class="result-box res-diff">Hiệu u - v: ({vec_diff[0]:.1f} ; {vec_diff[1]:.1f})</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Các chỉ số hình học
    m1, m2, m3 = st.columns(3)
    # Tùy chỉnh màu metric trong CSS nếu cần, mặc định Streamlit sẽ hiển thị trắng trên nền tối
    m1.metric("Tích vô hướng", f"{dot_product:.2f}")
    m2.metric("Độ dài |u|", f"{mag_u:.2f}")
    m3.metric("Độ dài |v|", f"{mag_v:.2f}")

    if mag_u > 0 and mag_v > 0:
        cos_phi = np.clip(dot_product / (mag_u * mag_v), -1.0, 1.0)
        angle = np.degrees(np.arccos(cos_phi))
        st.info(f"📐 Góc giữa hai vector: **{angle:.2f}°**")
