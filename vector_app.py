import streamlit as st
import numpy as np

st.set_page_config(page_title="Vector Engine", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0B0F19; }
    .vector-input { padding: 15px; border: 1px solid #1E293B; border-radius: 12px; background: #111827; margin-bottom: 10px;}
    </style>
""", unsafe_allow_html=True)

st.title("🧮 Xử Lý Tích Vô Hướng")

with st.container():
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="vector-input">', unsafe_allow_html=True)
        ux = st.number_input("Tọa độ x (u):", value=1.0)
        uy = st.number_input("Tọa độ y (u):", value=0.0)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="vector-input">', unsafe_allow_html=True)
        vx = st.number_input("Tọa độ x (v):", value=0.0)
        vy = st.number_input("Tọa độ y (v):", value=1.0)
        st.markdown('</div>', unsafe_allow_html=True)

if st.button("🚀 Khởi chạy tính toán", type="primary", use_container_width=True):
    u = np.array([ux, uy])
    v = np.array([vx, vy])
    dot = np.dot(u, v)
    st.divider()
    st.metric("Tích vô hướng u.v", f"{dot:.2f}")
