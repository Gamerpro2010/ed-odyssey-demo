import streamlit as st
import numpy as np

st.set_page_config(page_title="Vector Engine | ED-ODYSSEY", layout="wide")

st.markdown("""
    <style>
    /* Nền lưới tọa độ (Coordinate Grid Background) */
    .stApp {
        background-color: #0B0F19;
        background-image: 
            radial-gradient(circle, #1e293b 1px, transparent 1px),
            linear-gradient(to right, #161b22 1px, transparent 1px),
            linear-gradient(to bottom, #161b22 1px, transparent 1px);
        background-size: 40px 40px, 40px 40px, 40px 40px;
    }

    /* Đổi phông chữ toán học chuyên dụng */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;800&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'JetBrains+Mono', monospace;
    }

    .vector-header {
        font-size: 2.5rem; font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }

    .input-card {
        background: rgba(17, 24, 39, 0.8);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="vector-header">🧮 Xử Lý Tích Vô Hướng</div>', unsafe_allow_html=True)

with st.container():
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.subheader("Vector $\\vec{u}$")
        ux = st.number_input("Tọa độ x (u):", value=1.0, step=0.5)
        uy = st.number_input("Tọa độ y (u):", value=0.0, step=0.5)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.subheader("Vector $\\vec{v}$")
        vx = st.number_input("Tọa độ x (v):", value=0.0, step=0.5)
        vy = st.number_input("Tọa độ y (v):", value=1.0, step=0.5)
        st.markdown('</div>', unsafe_allow_html=True)

st.write("")
if st.button("🚀 Khởi chạy tính toán", type="primary", use_container_width=True):
    u = np.array([ux, uy])
    v = np.array([vx, vy])
    dot = np.dot(u, v)
    mag_u = np.linalg.norm(u)
    mag_v = np.linalg.norm(v)
    
    st.divider()
    res1, res2, res3 = st.columns(3)
    res1.metric("Tích vô hướng", f"{dot:.2f}")
    res2.metric("Độ dài |u|", f"{mag_u:.2f}")
    res3.metric("Độ dài |v|", f"{mag_v:.2f}")
