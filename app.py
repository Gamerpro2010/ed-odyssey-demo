import streamlit as st
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
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com" # Thay bằng email của bạn
SENDER_PASSWORD = "your_app_password"  # Thay bằng App Password của Google

def send_otp_email(receiver_email, otp_code):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        msg['Subject'] = "Mã xác thực ED-ODYSSEY"
        body = f"Mã xác thực của bạn là: {otp_code}. Vui lòng không chia sẻ mã này với bất kỳ ai."
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Lỗi gửi mail: {e}")
        return False

# ==========================================
# 1. QUẢN LÝ DATABASE (Nâng cấp cấu trúc)
# ==========================================
DB_FILE = 'users_db.json'
# Cấu trúc mới: {"username": {"pass": "...", "email": "...", "verified": False}}

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"admin": {"pass": "1234", "email": "", "verified": False}}

def save_db(db):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

# Khởi tạo session
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'current_user' not in st.session_state: st.session_state.current_user = ""
if 'temp_otp' not in st.session_state: st.session_state.temp_otp = ""

# ==========================================
# 2. GIAO DIỆN CHÍNH
# ==========================================
db = load_db()

if not st.session_state.logged_in:
    # --- MÀN HÌNH ĐĂNG NHẬP / QUÊN MẬT KHẨU ---
    st.title("🚀 ED-ODYSSEY")
    tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký"])
    
    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Vào hệ thống"):
                if u in db and db[u]['pass'] == p:
                    st.session_state.logged_in = True
                    st.session_state.current_user = u
                    st.rerun()
                else: st.error("Sai rồi!")
        with col2:
            with st.popover("Quên mật khẩu?"):
                st.write("Nhập Email đã liên kết để nhận lại mật khẩu")
                forgot_email = st.text_input("Email của bạn")
                if st.button("Gửi mật khẩu"):
                    # Tìm user có email này
                    found = False
                    for user, data in db.items():
                        if data.get('email') == forgot_email and data.get('verified'):
                            if send_otp_email(forgot_email, f"Mật khẩu của bạn là: {data['pass']}"):
                                st.success("Mật khẩu đã được gửi vào Email!")
                                found = True
                            break
                    if not found: st.error("Email chưa liên kết hoặc không tồn tại!")

    with tab2:
        new_u = st.text_input("Tạo Username")
        new_p = st.text_input("Tạo Password", type="password")
        if st.button("Đăng ký ngay"):
            if new_u in db: st.warning("Tên đã tồn tại")
            else:
                db[new_u] = {"pass": new_p, "email": "", "verified": False}
                save_db(db)
                st.success("Xong! Đăng nhập đi.")

else:
    # --- MÀN HÌNH SAU KHI ĐĂNG NHẬP ---
    with st.sidebar:
        st.write(f"Chào, **{st.session_state.current_user}**")
        menu = st.radio("Menu", ["Marketplace", "Cài đặt tài khoản"])
        if st.button("Đăng xuất"):
            st.session_state.logged_in = False
            st.rerun()

    if menu == "Cài đặt tài khoản":
        st.header("⚙️ Cài đặt & Liên kết Email")
        user_data = db[st.session_state.current_user]
        
        # Hiển thị trạng thái hiện tại
        if user_data['email'] and user_data['verified']:
            st.success(f"Đã liên kết: {user_data['email']}")
        else:
            st.warning("Tài khoản chưa được xác minh Email.")
            
        email_input = st.text_input("Nhập Email muốn liên kết", value=user_data['email'])
        
        col_verify, col_confirm = st.columns(2)
        
        with col_verify:
            if st.button("Gửi mã xác thực"):
                if "@" in email_input:
                    otp = "".join(random.choices(string.digits, k=6))
                    st.session_state.temp_otp = otp
                    if send_otp_email(email_input, otp):
                        st.info(f"Mã đã gửi đến {email_input}")
                    else: st.error("Gửi mail thất bại!")
                else: st.error("Email không hợp lệ")

        with col_confirm:
            otp_input = st.text_input("Nhập mã 6 số", placeholder="------")
            if st.button("Xác nhận liên kết"):
                if otp_input == st.session_state.temp_otp and otp_input != "":
                    db[st.session_state.current_user]['email'] = email_input
                    db[st.session_state.current_user]['verified'] = True
                    save_db(db)
                    st.success("Chúc mừng! Đã liên kết Email thành công.")
                    time.sleep(1)
                    st.rerun()
                else: st.error("Mã xác thực sai!")

    elif menu == "Marketplace":
        st.write("Đây là Marketplace của bạn...")
