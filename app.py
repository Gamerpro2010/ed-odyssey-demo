import streamlit as st
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components
import time
import json
import os
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# 0. CẤU HÌNH GỬI EMAIL (SMTP)
# ==========================================
# Nhớ tạo App Password trên Google để hệ thống gửi được mail thật nhé!
SENDER_EMAIL = "your_email@gmail.com" 
SENDER_PASSWORD = "your_app_password"

def send_mail(receiver, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except: return False

# ==========================================
# 1. CẤU HÌNH TRANG & CSS (FOUNDER EDITION)
# ==========================================
st.set_page_config(page_title="ED-ODYSSEY", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    .main-title { font-size: 2.6rem; font-weight: 900; color: #f8fafc; margin-bottom: 5px; letter-spacing: -0.5px; }
    .sub-title { color: #94a3b8; font-size: 1.1rem; margin-bottom: 35px; font-weight: 400;}
    
    /* Card Style cho Cài đặt & Marketplace */
    .cyber-card, .setting-card {
        background: #111827; border: 1px solid #1e293b; 
        border-radius: 16px; padding: 20px; margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .cyber-card:hover { border-color: #00FFFF; transform: translateY(-4px); }
    
    .status-badge { padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; }
    .verified { background: #065f46; color: #34d399; }
    .unverified { background: #7f1d1d; color: #f87171; }

    .founder-pass {
        background: linear-gradient(135deg, rgba(15,23,42,0.9) 0%, rgba(30,58,138,0.7) 100%);
        border: 1px solid rgba(0, 255, 255, 0.4); border-radius: 16px; padding: 22px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.6); margin-bottom: 25px;
    }
    .pass-balance { font-size: 2.6rem; font-weight: 900; color: #00FFFF; text-shadow: 0 0 15px rgba(0, 255, 255, 0.3); }
    
    /* Login Box */
    .login-box { background: #111827; padding: 40px; border-radius: 16px; border: 1px solid #1e293b; max-width: 500px; margin: 0 auto; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HỆ THỐNG DATABASE & SESSION
# ==========================================
DB_FILE = 'users_db.json'
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    return {"admin": {"pass": "1234", "email": "", "verified": False}}

def save_db(db_data):
    with open(DB_FILE, 'w', encoding='utf-8') as f: json.dump(db_data, f, ensure_ascii=False, indent=4)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'current_user' not in st.session_state: st.session_state.current_user = ""
if 'credit_balance' not in st.session_state: st.session_state.credit_balance = 50 
if 'owned_tools' not in st.session_state: st.session_state.owned_tools = []
if 'otp_code' not in st.session_state: st.session_state.otp_code = ""

db = load_db()

# ==========================================
# 3. GIAO DIỆN AUTHENTICATION
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; font-size: 3rem; font-weight: 900; color: #f8fafc; margin-top: 5vh;'>🚀 ED-ODYSSEY</h1>", unsafe_allow_html=True)
    col_a, col_main, col_b = st.columns([1, 2, 1])
    with col_main:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔑 Đăng nhập", "📝 Đăng ký"])
        
        with tab1:
            l_user = st.text_input("Username", key="li_u")
            l_pass = st.text_input("Password", type="password", key="li_p")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Đăng nhập", use_container_width=True, type="primary"):
                    if l_user in db and db[l_user]['pass'] == l_pass:
                        st.session_state.logged_in = True
                        st.session_state.current_user = l_user
                        st.rerun()
                    else: st.error("Sai thông tin!")
            with c2:
                with st.popover("Quên mật khẩu?", use_container_width=True):
                    st.write("### Hỗ trợ khôi phục")
                    target = st.text_input("Nhập email đã liên kết:")
                    if st.button("Gửi mật khẩu qua Email"):
                        found = False
                        for user, data in db.items():
                            if data.get('email') == target and data.get('verified'):
                                send_mail(target, "Khôi phục mật khẩu ED-ODYSSEY", f"Mật khẩu của bạn là: {data['pass']}")
                                st.success("Đã gửi! Hãy check mail.")
                                found = True; break
                        if not found: st.error("Email chưa xác minh!")
        
        with tab2:
            n_user = st.text_input("Username mới", key="re_u")
            n_pass = st.text_input("Password mới", type="password", key="re_p")
            if st.button("Tạo tài khoản", use_container_width=True):
                if n_user in db: st.error("Đã tồn tại!")
                else:
                    db[n_user] = {"pass": n_pass, "email": "", "verified": False}
                    save_db(db); st.success("Đăng ký thành công!")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 4. GIAO DIỆN NỀN TẢNG CHÍNH
# ==========================================
else:
    with st.sidebar:
        st.markdown(f"""<div class="founder-pass">
            <div style="font-size:0.7rem; color:#94a3b8;">Hệ thống Ody-Credit</div>
            <div class="pass-balance">{st.session_state.credit_balance} <span style="font-size:1rem; color:#fff;">CR</span></div>
            <div style="font-size:0.9rem; font-weight:800; color:#f8fafc; margin-top:15px;">👤 {st.session_state.current_user.upper()}</div>
        </div>""", unsafe_allow_html=True)
        
        if st.button("💳 Nạp Credit (100 CR)", use_container_width=True):
            st.session_state.credit_balance += 100
            st.rerun()
            
        st.write("---")
        menu = st.radio("ĐIỀU HƯỚNG", ["🛒 Marketplace", "💻 My Workspace", "⚙️ Cài đặt tài khoản"])
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # --- MENU: MARKETPLACE ---
    if menu == "🛒 Marketplace":
        st.markdown('<div class="main-title">Blueprint Marketplace</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-title">Trang bị các mô-đun công nghệ giáo dục chuyên sâu.</div>', unsafe_allow_html=True)
        
        m_col1, m_col2 = st.columns(2, gap="medium")
        tools = [
            ("Mô Phỏng Vật Lý 10", 15, "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=400"),
            ("3D Vector & Oxyz Lab", 20, "https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?w=400"),
            ("Xử Lý Tích Vô Hướng", 12, "https://images.unsplash.com/photo-1509228641021-f883935a4d7b?w=400"),
            ("Thống Kê Dữ Liệu", 10, "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400")
        ]
        
        for i, (name, price, img) in enumerate(tools):
            target_col = m_col1 if i % 2 == 0 else m_col2
            with target_col:
                st.markdown(f"""<div class="cyber-card">
                    <img src="{img}" style="width:100%; border-radius:12px; margin-bottom:15px; height:180px; object-fit:cover;">
                    <div style="font-size:1.2rem; font-weight:800; color:#f8fafc;">{name}</div>
                    <div style="color:#0ea5e9; font-size:0.8rem; font-weight:800;">BY ED-ODYSSEY</div>
                    <div style="font-size:1.4rem; font-weight:900; color:#fff; margin-top:10px;">{price} CR</div>
                </div>""", unsafe_allow_html=True)
                if st.button(f"Mua {name}", key=f"buy_{i}", use_container_width=True):
                    if name in st.session_state.owned_tools: st.toast(f"Đã sở hữu {name}!")
                    elif st.session_state.credit_balance >= price:
                        st.session_state.credit_balance -= price
                        st.session_state.owned_tools.append(name)
                        st.balloons(); st.rerun()
                    else: st.error("Không đủ Credit!")

    # --- MENU: WORKSPACE ---
    elif menu == "💻 My Workspace":
        st.markdown('<div class="main-title">My Workspace</div>', unsafe_allow_html=True)
        if not st.session_state.owned_tools: st.info("Bàn làm việc trống. Hãy mua công cụ từ Marketplace!")
        else:
            tabs = st.tabs(st.session_state.owned_tools)
            links = {
                "Mô Phỏng Vật Lý 10": "https://mo-phong-vat-ly-10.streamlit.app/?embed=true",
                "3D Vector & Oxyz Lab": "https://3d-vector-va-do-thi.streamlit.app/?embed=true",
                "Xử Lý Tích Vô Hướng": "https://tich-vo-huong.streamlit.app/?embed=true",
                "Thống Kê Dữ Liệu": "https://thong-ke.streamlit.app/?embed=true"
            }
            for i, tool in enumerate(st.session_state.owned_tools):
                with tabs[i]: components.iframe(links[tool], height=800, scrolling=True)

    # --- MENU: CÀI ĐẶT ---
    elif menu == "⚙️ Cài đặt tài khoản":
        st.markdown('<div class="main-title">Thiết lập tài khoản</div>', unsafe_allow_html=True)
        user_data = db[st.session_state.current_user]
        
        st.markdown('<div class="setting-card">', unsafe_allow_html=True)
        st.subheader("📧 Liên kết Email & Bảo mật")
        status_html = '<span class="status-badge verified">Đã xác minh</span>' if user_data['verified'] else '<span class="status-badge unverified">Chưa xác minh</span>'
        st.markdown(f"Trạng thái: {status_html}", unsafe_allow_html=True)
        
        email_val = st.text_input("Địa chỉ Email", value=user_data['email'], placeholder="example@gmail.com")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📤 Gửi mã OTP", use_container_width=True):
                if "@" in email_val:
                    st.session_state.otp_code = "".join(random.choices(string.digits, k=6))
                    if send_mail(email_val, "Mã xác thực ED-ODYSSEY", f"Mã của bạn là: {st.session_state.otp_code}"):
                        st.toast("Mã OTP đã gửi!", icon="✅")
                    else: st.error("Lỗi gửi mail!")
        with c2:
            otp_in = st.text_input("Nhập mã OTP", placeholder="6 chữ số", label_visibility="collapsed")
            if st.button("✅ Xác thực & Liên kết", use_container_width=True, type="primary"):
                if otp_in == st.session_state.otp_code and otp_in != "":
                    db[st.session_state.current_user]['email'] = email_val
                    db[st.session_state.current_user]['verified'] = True
                    save_db(db); st.success("Thành công!"); time.sleep(1); st.rerun()
                else: st.error("Mã sai!")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="setting-card">', unsafe_allow_html=True)
        st.subheader("🔑 Đổi mật khẩu")
        new_p = st.text_input("Mật khẩu mới", type="password")
        if st.button("Cập nhật mật khẩu", use_container_width=True):
            db[st.session_state.current_user]['pass'] = new_p
            save_db(db); st.toast("Đã thay đổi!", icon="🔐")
        st.markdown('</div>', unsafe_allow_html=True)
