import streamlit as st
import numpy as np

st.set_page_config(page_title="Vector Engine | ED-ODYSSEY", layout="wide")

st.markdown("""
    <style>
    /* Nền lưới tọa độ Graph Paper */
    .stApp {
        background-color: #0B0F19;
        background-image: 
            linear-gradient(rgba(56, 189, 248, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(56, 189, 248, 0.1) 1px, transparent 1px);
        background-size: 30px 30px;
    }

    /* Phông chữ kỹ thuật JetBrains Mono */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;800&display=swap');
    html, body, [class*="st-"] { font-family: 'JetBrains+Mono', monospace; }

    .vector-header {
        font-size: 2.5rem; font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 25px;
    }
    .input-card {
        background: rgba(17, 24, 39, 0.85);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(8px);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="vector-header">🧮 Vector Coordinate Engine</div>', unsafe_allow_html=True)

with st.container():
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.subheader("Vector $\\vec{u}$")
        ux = st.number_input("Hoành độ x(u):", value=2.0, step=0.5)
        uy = st.number_input("Tung độ y(u):", value=3.0, step=0.5)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.subheader("Vector $\\vec{v}$")
        vx = st.number_input("Hoành độ x(v):", value=1.0, step=0.5)
        vy = st.number_input("Tung độ y(v):", value=-2.0, step=0.5)
        st.markdown('</div>', unsafe_allow_html=True)

st.write("")
if st.button("🚀 Thực thi phép toán Vector", type="primary", use_container_width=True):
    u = np.array([ux, uy])
    v = np.array([vx, vy])
    
    # Tính toán mở rộng
    vec_sum = u + v
    vec_diff = u - v
    dot_product = np.dot(u, v)
    mag_u = np.linalg.norm(u)
    mag_v = np.linalg.norm(v)

    st.divider()
    
    # Hiển thị kết quả tọa độ
    res_a, res_b = st.columns(2)
    res_a.success(f"**Tổng $\\vec{u} + \\vec{v}$**: ({vec_sum[0]:.1f} ; {vec_sum[1]:.1f})")
    res_b.info(f"**Hiệu $\\vec{u} - \\vec{v}$**: ({vec_diff[0]:.1f} ; {vec_diff[1]:.1f})")
    
    st.write("")
    
    # Chỉ số hình học
    m1, m2, m3 = st.columns(3)
    m1.metric("Tích vô hướng", f"{dot_product:.2f}")
    m2.metric("Độ dài |u|", f"{mag_u:.2f}")
    m3.metric("Độ dài |v|", f"{mag_v:.2f}")

    if mag_u > 0 and mag_v > 0:
        angle = np.degrees(np.arccos(np.clip(dot_product/(mag_u*mag_v), -1, 1)))
        st.info(f"📐 Góc giữa hai vector: **{angle:.2f}°**")
