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
    /* Nền đen nhám mã hex #0E1117 chuẩn phong cách Coder */
    .stApp { background-color: #0E1117; }
    .block-container { padding-top: 2rem; max-width: 1200px; } 
    
    /* Tiêu đề chính sử dụng phong cách Hustle Hub */
    .main-title { 
        font-size: 2.6rem; font-weight: 900; color: #f8fafc; 
        margin-bottom: 5px; letter-spacing: -0.5px;
    }
    .sub-title { color: #94a3b8; font-size: 1.1rem; margin-bottom: 35px; font-weight: 400;}

    /* THIẾT KẾ THẺ NGUYÊN KHỐI (MONOLITHIC CARD) */
    .cyber-card {
        background: #111827; border: 1px solid #1e293b; border-bottom: none; 
        border-radius: 16px 16px 0 0; overflow: hidden; display: flex; flex-direction: column;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    div[data-testid="column"]:hover .cyber-card { border-color: #00FFFF; transform: translateY(-4px); }
    div[data-testid="column"]:hover div.stButton > button { 
        transform: translateY(-4px); 
        box-shadow: 0 12px 25px -5px rgba(0, 255, 255, 0.4) !important; 
        filter: brightness(1.1); 
    }

    .img-wrapper { width: 100%; height: 160px; border-bottom: 1px solid #1e293b; background-color: #0f172a; }
    .img-wrapper img { width: 100%; height: 100%; object-fit: cover; object-position: center; }
    
    .card-content { padding: 18px; display: flex; flex-direction: column; }
    .c-title { font-size: 1.15rem; font-weight: 800; color: #f8fafc; margin-bottom: 4px; }
    .c-author { 
        font-size: 0.7rem; color: #0ea5e9; text-transform: uppercase; 
        font-weight: 800; letter-spacing: 0.5px; margin-bottom: 10px; 
    }
    .c-desc { font-size: 0.8rem; color: #cbd5e1; line-height: 1.5; height: 50px; overflow: hidden;}
    .c-price { font-size: 1.3rem; font-weight: 900; color: #fff; margin-top: 10px; }

    /* NÚT BẤM MÀU NEON DÍNH VÀO THẺ */
    div.stButton > button {
        background: linear-gradient(90deg, #0284c7 0%, #00FFFF 100%) !important;
        border: none !important; color: #0E1117 !important; font-weight: 800 !important; font-size: 1rem !important;
        border-radius: 0 0 16px 16px !important; padding: 12px !important; width: 100% !important;
        margin-top: -15px !important; transition: all 0.3s ease !important;
    }

    /* THẺ ID BÊN SIDEBAR - HOLOGRAM EFFECT */
    .founder-pass {
        background: linear-gradient(135deg, rgba(15,23,42,0.9) 0%, rgba(30,58,138,0.7) 100%);
        border: 1px solid rgba(0, 255, 255, 0.4); border-radius: 16px; padding: 22px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.6); margin-bottom: 25px;
    }
    .pass-header { font-size: 0.7rem; color: #94a3b8; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 12px; }
    .pass-balance { 
        font-size: 2.6rem; font-weight: 900; color: #00FFFF; 
        line-height: 1; text-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
    }
    .pass-currency { font-size: 1rem; color: #e2e8f0; font-weight: 500; }
    .pass-user { font-size: 0.95rem; color: #f8fafc; font-weight: 800; margin-top: 18px; letter-spacing: 1px; text-transform: uppercase; }
    .pass-id { font-size: 0.75rem; color: #64748b; font-family: monospace; margin-top: 5px; }
    
    /* Box Login */
    .login-box { 
        background: #111827; padding: 40px; border-radius: 16px; 
        border: 1px solid #1e293b; max-width: 500px; margin: 0 auto; 
        margin-top: 50px; box-shadow: 0 20px 40px rgba(0,0,0,0.5); 
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HỆ THỐNG CƠ SỞ DỮ LIỆU (JSON DATABASE)
# ==========================================
DB_FILE = 'users_db.json'
DEFAULT_USERS = {'admin': '1234', 'honamson': 'honamson2010'}

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return DEFAULT_USERS
    return DEFAULT_USERS

def save_db(db_data):
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(db_data, f, ensure_ascii=False, indent=4)
    except Exception:
        pass

if 'users_db' not in st.session_state:
    st.session_state.users_db = load_db() 
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
    
if 'credit_balance' not in st.session_state:
    st.session_state.credit_balance = 50 
if 'owned_tools' not in st.session_state:
    st.session_state.owned_tools = []
if 'show_success' not in st.session_state:
    st.session_state.show_success = None

# ==========================================
# 4. GIAO DIỆN AUTHENTICATION
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; font-size: 3rem; font-weight: 900; color: #f8fafc; margin-top: 5vh;'>🚀 ED-ODYSSEY</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Hành trình tri thức kiến tạo từ sự sẻ chia</p>", unsafe_allow_html=True)
    
    col_a, col_main, col_b = st.columns([1, 2, 1])
    with col_main:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔑 Đăng nhập", "📝 Đăng ký"])
        
        with tab1:
            login_user = st.text_input("Tên đăng nhập")
            login_pass = st.text_input("Mật khẩu", type="password")
            if st.button("Đăng nhập vào hệ thống", use_container_width=True):
                st.session_state.users_db = load_db()
                if login_user in st.session_state.users_db and st.session_state.users_db[login_user] == login_pass:
                    st.session_state.logged_in = True
                    st.session_state.current_user = login_user
                    st.rerun()
                else:
                    st.error("Sai tên đăng nhập hoặc mật khẩu!")
                    
        with tab2:
            new_user = st.text_input("Tạo tên hiển thị (Ví dụ: NguyenVanA)")
            new_pass = st.text_input("Tạo mật khẩu", type="password")
            if st.button("Tạo tài khoản mới", use_container_width=True):
                st.session_state.users_db = load_db()
                if new_user == "" or new_pass == "":
                    st.warning("Vui lòng điền đủ thông tin!")
                elif new_user in st.session_state.users_db:
                    st.error("Tên đăng nhập này đã tồn tại!")
                else:
                    st.session_state.users_db[new_user] = new_pass
                    save_db(st.session_state.users_db)
                    st.session_state.logged_in = True
                    st.session_state.current_user = new_user
                    st.toast("Đăng ký thành công!", icon="✅")
                    time.sleep(0.5)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 5. GIAO DIỆN NỀN TẢNG CHÍNH
# ==========================================
else:
    if st.session_state.show_success:
        st.toast(f"Mở khóa thành công: {st.session_state.show_success}", icon="✅")
        st.balloons()
        st.session_state.show_success = None

    def process_purchase(tool_name, price):
        if tool_name in st.session_state.owned_tools:
            st.toast(f"Bạn đã sở hữu {tool_name}!", icon="ℹ️")
        elif st.session_state.credit_balance >= price:
            st.session_state.credit_balance -= price
            st.session_state.owned_tools.append(tool_name)
            st.session_state.show_success = tool_name
            st.rerun() 
        else:
            st.error("Số dư Credit không đủ!")

    with st.sidebar:
        st.markdown("## 🚀 ED-ODYSSEY")
        st.write("---")
        
        st.markdown(f"""
            <div class="founder-pass">
                <div class="pass-header">Hệ thống Ody-Credit</div>
                <div class="pass-balance">{st.session_state.credit_balance} <span class="pass-currency">CR</span></div>
                <div class="pass-user">{st.session_state.current_user}</div>
                <div class="pass-id">ID: {hash(st.session_state.current_user) % 100000}-EXPLORER</div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.popover("💳 Nạp Năng Lượng (CR)", use_container_width=True):
            amount = st.number_input("Số CR muốn nạp", min_value=10, step=10, value=20)
            if st.button("Xác nhận nạp", type="primary", use_container_width=True):
                st.session_state.credit_balance += amount
                st.rerun()

        st.write("---")
        menu = st.radio("ĐIỀU HƯỚNG", ["🛒 Marketplace", "💻 My Workspace", "🎯 Bounty Board"], label_visibility="collapsed")
        
        st.write("---")
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    if menu == "🛒 Marketplace":
        st.markdown('<div class="main-title">Blueprint Marketplace</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-title">Trang bị các mô-đun công nghệ giáo dục chuyên sâu.</div>', unsafe_allow_html=True)
        
        # HÀNG 1
        col1, col2 = st.columns(2, gap="medium")
        with col1:
            st.markdown("""<div class="cyber-card">
                <div class="img-wrapper"><img src="https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?auto=format&fit=crop&q=80&w=800"></div>
                <div class="card-content">
                    <div class="c-title">Mô Phỏng Vật Lý 10</div>
                    <div class="c-author">BY ED-ODYSSEY</div>
                    <div class="c-desc">Giả lập ném xiên và động học chất điểm tương tác thời gian thực[cite: 223].</div>
                    <div class="c-price">15 CR</div>
                </div></div>""", unsafe_allow_html=True)
            if st.button("Mua gói vĩnh viễn", key="buy_phy", use_container_width=True):
                process_purchase("Mô Phỏng Vật Lý 10", 15)

        with col2:
            st.markdown("""<div class="cyber-card">
                <div class="img-wrapper"><img src="https://images.unsplash.com/photo-1509228641021-f883935a4d7b?auto=format&fit=crop&q=80&w=800"></div>
                <div class="card-content">
                    <div class="c-title">3D Vector & Oxyz Lab</div>
                    <div class="c-author">BY MATHWIZ_HNS</div>
                    <div class="c-desc">Phòng thí nghiệm hình học không gian 3D tương tác đa biến[cite: 210, 211].</div>
                    <div class="c-price">20 CR</div>
                </div></div>""", unsafe_allow_html=True)
            if st.button("Mua gói vĩnh viễn", key="buy_3d", use_container_width=True):
                process_purchase("3D Vector & Oxyz Lab", 20)

        st.write("")
        # HÀNG 2
        col3, col4 = st.columns(2, gap="medium")
        with col3:
            st.markdown("""<div class="cyber-card">
                <div class="img-wrapper"><img src="https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&q=80&w=800"></div>
                <div class="card-content">
                    <div class="c-title">Xử Lý Tích Vô Hướng</div>
                    <div class="c-author">BY CODENINJA_HNS</div>
                    <div class="c-desc">Engine xử lý ma trận và giải nhanh các phép toán vector đại số bằng NumPy[cite: 204, 227].</div>
                    <div class="c-price">12 CR</div>
                </div></div>""", unsafe_allow_html=True)
            if st.button("Mua gói vĩnh viễn", key="buy_vec", use_container_width=True):
                process_purchase("Xử Lý Tích Vô Hướng", 12)

        with col4:
            st.markdown("""<div class="cyber-card">
                <div class="img-wrapper"><img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=800"></div>
                <div class="card-content">
                    <div class="c-title">Thống Kê Dữ Liệu</div>
                    <div class="c-author">By DATA_MASTER</div>
                    <div class="c-desc">Công cụ vẽ biểu đồ và phân tích xác suất thống kê thực hành qua Plotly[cite: 208, 226].</div>
                    <div class="c-price">10 CR</div>
                </div></div>""", unsafe_allow_html=True)
            if st.button("Mua gói vĩnh viễn", key="buy_stat", use_container_width=True):
                process_purchase("Thống Kê Dữ Liệu", 10)

    elif menu == "💻 My Workspace":
        st.markdown('<div class="main-title">My Workspace</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sub-title">Bàn làm việc của {st.session_state.current_user}.</div>', unsafe_allow_html=True)
        
        if not st.session_state.owned_tools:
            st.info("Bàn làm việc trống. Hãy mua công cụ từ Marketplace!")
        else:
            tabs = st.tabs(st.session_state.owned_tools)
            for i, tool in enumerate(st.session_state.owned_tools):
                with tabs[i]:
                    st.write("") 
                    if tool == "Mô Phỏng Vật Lý 10":
                        components.iframe("https://mo-phong-vat-ly-10.streamlit.app/?embed=true", height=900, scrolling=True)
                    elif tool == "3D Vector & Oxyz Lab":
                        components.iframe("https://3d-vector-va-do-thi.streamlit.app/?embed=true", height=1000, scrolling=True)
                    elif tool == "Xử Lý Tích Vô Hướng":
                        components.iframe("https://tich-vo-huong.streamlit.app/?embed=true", height=900, scrolling=True)
                    elif tool == "Thống Kê Dữ Liệu":
                        components.iframe("https://thong-ke.streamlit.app/?embed=true", height=900, scrolling=True)

    elif menu == "🎯 Bounty Board":
        st.markdown('<div class="main-title">Bounty Board</div>', unsafe_allow_html=True)
        st.info("Hệ thống nhiệm vụ đang được bảo trì[cite: 242].")
