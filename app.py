import streamlit as st
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components
import time
import json
import os

# ==========================================
# 1. CẤU HÌNH TRANG - ED-ODYSSEY
# ==========================================
st.set_page_config(page_title="ED-ODYSSEY", page_icon="🚀", layout="wide")

# ==========================================
# 2. CSS CAO CẤP (FOUNDER EDITION UI)
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    .block-container { padding-top: 2rem; max-width: 1200px; } 
    .main-title { font-size: 2.6rem; font-weight: 900; color: #f8fafc; margin-bottom: 5px; }
    .sub-title { color: #94a3b8; font-size: 1.1rem; margin-bottom: 35px; }
    .login-box {
        background: #1e293b;
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #334155;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. QUẢN LÝ DỮ LIỆU NGƯỜI DÙNG
# ==========================================
DB_FILE = "users_db.json"
DEFAULT_USERS = {"admin": "1234", "guest": "guest123", "honamson": "honamson2010"}

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_USERS

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'owned_tools' not in st.session_state:
    st.session_state.owned_tools = []

# ==========================================
# 4. GIAO DIỆN AUTHENTICATION (ĐÃ CẬP NHẬT)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; font-size: 3rem; font-weight: 900; color: #f8fafc; margin-top: 5vh;'>🚀 ED-ODYSSEY</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Hành trình tri thức kiến tạo từ sự sẻ chia</p>", unsafe_allow_html=True)
    
    col_a, col_main, col_b = st.columns([1, 2, 1])
    with col_main:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔑 Đăng nhập", "📝 Đăng ký"])
        
        with tab1:
            login_user = st.text_input("Tên đăng nhập", placeholder="Nhập username...", key="li_u")
            login_pass = st.text_input("Mật khẩu", type="password", placeholder="Nhập password...", key="li_p")
            
            # Layout cho nút bấm
            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button("Đăng nhập", use_container_width=True, type="primary"):
                    db = load_db()
                    if login_user in db and db[login_user] == login_pass:
                        st.session_state.logged_in = True
                        st.session_state.current_user = login_user
                        st.rerun()
                    else:
                        st.error("Thông tin không chính xác!")
            
            with c2:
                # TÍNH NĂNG MỚI NÈ: QUÊN MẬT KHẨU
                with st.popover("❓ Quên thông tin?", use_container_width=True):
                    st.write("### Khôi phục tài khoản")
                    issue = st.radio("Bạn quên gì?", ["Mật khẩu", "Tên đăng nhập"])
                    info_input = st.text_input("Nhập Tên tài khoản hoặc Email:")
                    if st.button("Gửi yêu cầu", use_container_width=True):
                        if info_input:
                            st.success(f"Yêu cầu xử lý '{info_input}' đã được gửi tới Admin!")
                            st.toast("Hãy check Discord/Zalo của Admin nhé!", icon="📩")
                        else:
                            st.warning("Nhập thông tin đã chứ!")

        with tab2:
            new_user = st.text_input("Tạo username", key="reg_u")
            new_pass = st.text_input("Tạo mật khẩu", type="password", key="reg_p")
            if st.button("Tạo tài khoản", use_container_width=True):
                db = load_db()
                if new_user in db:
                    st.error("Tên này có người lấy rồi!")
                elif new_user and new_pass:
                    db[new_user] = new_pass
                    save_db(db)
                    st.success("Đăng ký xong! Qua tab Đăng nhập thôi.")
                else:
                    st.warning("Điền đủ thông tin đi bạn ơi!")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 5. GIAO DIỆN CHÍNH (KHI ĐÃ LOGGED IN)
# ==========================================
else:
    # Sidebar và các tính năng khác giữ nguyên như cũ
    with st.sidebar:
        st.markdown(f"### Chào, {st.session_state.current_user}!")
        if st.button("Đăng xuất"):
            st.session_state.logged_in = False
            st.rerun()
            
    st.markdown('<div class="main-title">Bảng điều khiển</div>', unsafe_allow_html=True)
    st.write("Chào mừng bạn quay trở lại với ED-ODYSSEY!")
    # ... (Các phần code Marketplace và Workspace của bạn tiếp tục ở đây)
