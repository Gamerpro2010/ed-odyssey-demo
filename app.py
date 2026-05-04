import streamlit as st
import time

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="ED-ODYSSEY MVP", page_icon="🚀", layout="centered")

# --- KHỞI TẠO DỮ LIỆU TẠM THỜI (Giả lập Database) ---
if 'credit' not in st.session_state:
    st.session_state.credit = 50 # Tặng sẵn 50 điểm làm vốn

# --- GIAO DIỆN CHÍNH ---
st.title("🚀 ED-ODYSSEY")
st.subheader("Hành trình tri thức kiến tạo từ sự sẻ chia")
st.info(f"💳 Số dư Credit hiện tại của bạn: **{st.session_state.credit} Credit**")

# Tạo 3 Tab chức năng
tab1, tab2, tab3 = st.tabs(["🛒 Chợ Giao Dịch", "🧠 Cày Credit", "🤖 AI Tạo Đề (Free)"])

# --- TAB 1: CHỢ GIAO DỊCH (Tiêu Credit) ---
with tab1:
    st.markdown("### 📌 Bảng tin Nhiệm vụ")
    
    # Task 1
    with st.container(border=True):
        st.write("**[IELTS]** Cần người nhận xét chi tiết bài IELTS Writing Task 1 dạng Line Graph. Target band 6.0.")
        st.caption("Treo thưởng: 30 Credit | Đăng bởi: User_Ngan123")
        if st.button("Nhận kèo (Task 1)"):
            st.success("Nhận kèo thành công! Hãy liên hệ qua khung chat nhóm.")
            
    # Task 2
    with st.container(border=True):
        st.write("**[Toán 10]** Giải thích giúp mình câu 2 trắc nghiệm phần Đại số tổ hợp, mình hay bị nhầm chỗ này.")
        st.caption("Treo thưởng: 15 Credit | Đăng bởi: User_Thao456")
        if st.button("Nhận kèo (Task 2)"):
            st.success("Nhận kèo thành công! 15 Credit sẽ được cộng sau khi xác nhận hoàn thành.")

# --- TAB 2: CÀY CREDIT (Học bằng kỹ thuật Feynman) ---
with tab2:
    st.markdown("### 📝 Dùng AI chấm điểm Tóm tắt kiến thức")
    st.write("Viết lại một kiến thức bạn vừa học theo cách hiểu của mình. Nếu AI đánh giá cao, bạn sẽ nhận được Credit!")
    
    chu_de = st.selectbox("Chọn chủ đề bạn muốn tóm tắt:", ["Vật lý 10 - Nhiệt động lực học", "Toán 10 - Hình học tọa độ", "Địa lý - Hệ tọa độ địa lý"])
    noi_dung = st.text_area("Nhập nội dung tóm tắt của bạn vào đây:", height=150)
    
    if st.button("Gửi AI chấm điểm"):
        if noi_dung == "":
            st.warning("Vui lòng nhập nội dung trước khi gửi!")
        else:
            with st.spinner('AI đang đọc và đánh giá bài của bạn...'):
                time.sleep(2) # Giả lập thời gian chờ API
                st.success("🎉 Xuất sắc! Cách giải thích rất dễ hiểu và logic.")
                st.session_state.credit += 20
                st.balloons()
                st.info("Bạn được cộng +20 Credit!")

# --- TAB 3: AI TẠO ĐỀ (Sinh dữ liệu 0 đồng) ---
with tab3:
    st.markdown("### 🎲 Thử thách kiến thức ngẫu nhiên")
    st.write("Dùng AI tự động sinh ra đề bài mới 100% để luyện tập, không lo vi phạm bản quyền sách!")
    
    mon_hoc = st.selectbox("Chọn môn học:", ["Toán học", "Vật lý", "Tiếng Anh (IELTS)"])
    do_kho = st.radio("Mức độ:", ["Cơ bản", "Vận dụng cao"], horizontal=True)
    
    if st.button("Tạo đề ngay"):
        with st.spinner("Đang chế tạo đề thi..."):
            time.sleep(1.5)
            st.markdown("---")
            if mon_hoc == "Tiếng Anh (IELTS)":
                st.write("🔥 **Đề bài:** Some people think that in the modern world we are more dependent on each other, while others think that people have become more independent. Discuss both views and give your own opinion.")
            else:
                st.write("🔥 **Đề bài:** Một bài toán/lý cực hay vừa được AI sáng tác dành riêng cho bạn!")
            
            st.button("Dùng 5 Credit để xem Đáp án / Bài mẫu")