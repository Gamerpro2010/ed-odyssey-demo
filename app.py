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
    .main-title { font-size: 2.6rem; font-weight: 900; color: #f8fafc; margin-bottom: 5px; letter-spacing: -0.5px; }
    .sub-title { color: #94a3b8; font-size: 1.1rem; margin-bottom: 35px; font-weight: 400;}
    .cyber-card {
        background: #111827; border: 1px solid #1e293b; border-bottom: none; 
        border-radius: 16px 16px 0 0; overflow: hidden; display: flex; flex-direction: column;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    div[data-testid="column"]:hover .cyber-card { border-color: #00FFFF; transform: translateY(-4px); }
    .img-wrapper { width: 100%; height: 160px; border-bottom: 1px solid #1e293b; background-color: #0f172a; }
    .img-wrapper img { width: 100%; height: 100%; object-fit: cover; }
    .card-content { padding: 18px; }
    .c-title { font-size: 1.15rem; font-weight: 800; color: #f8fafc; margin-bottom: 4px; }
    .c-author { font-size: 0.7rem; color: #0ea5e9; text-transform: uppercase; font-weight: 800; margin-bottom: 10px; }
    .c-desc { font-size: 0.8rem; color: #cbd5e1; line-height: 1.5; height: 50px; overflow: hidden;}
    .c-price { font-size: 1.3rem; font-weight: 900; color: #fff; margin-top: 10px; }
    div.stButton > button {
        background: linear-gradient(90deg, #0284c7 0%, #00FFFF 100%) !important;
        border: none !important; color: #0E1117 !important; font-weight: 800 !important;
        border-radius: 0 0 16px 16px !important; padding: 12px !important; width: 100% !important;
        margin-top: -15px !important; transition: all 0.3s ease !important;
    }
    .founder-pass {
        background: linear-gradient(135deg, rgba(15,23,42,0.9) 0%, rgba(30,58,138,0.7) 100%);
        border: 1px solid rgba(0, 255, 255, 0.4); border-radius: 16px; padding: 22px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.6); margin-bottom: 25px;
    }
    .pass-balance { font-size: 2.6rem; font-weight: 900; color: #00FFFF; text-shadow: 0 0 15px rgba(0, 255, 255, 0.3); }
    .login-box { background: #111827; padding: 40px; border-radius: 16px; border: 1px solid #1e293b; max-width: 500px; margin: 0 auto; margin-top: 50px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HỆ THỐNG DỮ LIỆU NGƯỜI DÙNG
# ==========================================
DB_FILE = 'users_db.json'
DEFAULT_USERS = {'admin': '1234', 'honamson': 'honamson2010'}

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)
        except: return DEFAULT_USERS
    return DEFAULT_USERS

def save_db(db_data):
    with open(DB_FILE, 'w', encoding='utf-8') as f: json.dump(db_data, f, ensure_ascii=False, indent=4)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'current_user' not in st.session_state: st.session_state.current_user = ""
if 'credit_balance' not in st.session_state: st.session_state.credit_balance = 50 
if 'owned_tools' not in st.session_state: st.session_state.owned_tools = []

# ==========================================
# 4. GIAO DIỆN AUTHENTICATION (CÓ QUÊN MẬT KHẨU)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; font-size: 3rem; font-weight: 900; color: #f8fafc; margin-top: 5vh;'>🚀 ED-ODYSSEY</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Hành trình tri thức kiến tạo từ sự sẻ chia</p>", unsafe_allow_html=True)
    
    col_a, col_main, col_b = st.columns([1, 2, 1])
    with col_main:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔑 Đăng nhập", "📝 Đăng ký"])
        
        with tab1:
            l_user = st.text_input("Tên đăng nhập", key="login_u")
            l_pass = st.text_input("Mật khẩu", type="password", key="login_p")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Đăng nhập", use_container_width=True, type="primary"):
                    db = load_db()
                    if l_user in db and db[l_user] == l_pass:
                        st.session_state.logged_in = True
                        st.session_state.current_user = l_user
                        st.rerun()
                    else: st.error("Sai thông tin!")
            with c2:
                with st.popover("❓ Quên mật khẩu?", use_container_width=True):
                    st.write("### Hỗ trợ khôi phục")
                    target = st.text_input("Nhập username/email:")
                    if st.button("Gửi yêu cầu"):
                        st.toast(f"Đã gửi yêu cầu cho {target}!", icon="📩")
        
        with tab2:
            n_user = st.text_input("Tên hiển thị", key="reg_u")
            n_pass = st.text_input("Mật khẩu", type="password", key="reg_p")
            if st.button("Tạo tài khoản", use_container_width=True):
                db = load_db()
                if n_user in db: st.error("Đã tồn tại!")
                elif n_user and n_pass:
                    db[n_user] = n_pass
                    save_db(db)
                    st.success("Đăng ký thành công! Hãy qua tab Đăng nhập.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 5. GIAO DIỆN NỀN TẢNG CHÍNH (FULL)
# ==========================================
else:
    def process_purchase(name, price):
        if name in st.session_state.owned_tools: st.toast(f"Đã sở hữu {name}!")
        elif st.session_state.credit_balance >= price:
            st.session_state.credit_balance -= price
            st.session_state.owned_tools.append(name)
            st.balloons()
            st.rerun()
        else: st.error("Không đủ Credit!")

    with st.sidebar:
        st.markdown("## 🚀 ED-ODYSSEY")
        st.markdown(f"""<div class="founder-pass">
            <div style="font-size:0.7rem; color:#94a3b8;">Hệ thống Ody-Credit</div>
            <div class="pass-balance">{st.session_state.credit_balance} <span style="font-size:1rem; color:#fff;">CR</span></div>
            <div style="font-size:0.9rem; font-weight:800; color:#f8fafc; margin-top:15px;">{st.session_state.current_user.upper()}</div>
        </div>""", unsafe_allow_html=True)
        
        if st.button("💳 Nạp Credit (100 CR)", use_container_width=True):
            st.session_state.credit_balance += 100
            st.rerun()
            
        st.write("---")
        menu = st.radio("ĐIỀU HƯỚNG", ["🛒 Marketplace", "💻 My Workspace", "🎯 Bounty Board"])
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state.logged_in = False
