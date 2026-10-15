import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cấu hình trang web
st.set_page_config(page_title="Quản Lý Điểm Sinh Viên", layout="wide")

# 1. Hiển thị tiêu đề Web App
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# 2. Tạo DataFrame dữ liệu 10 sinh viên cập nhật theo Colab
data = {
    'Họ và tên': ['Phiến', 'Tình', 'Trĩ', 'Dũ', 'Hã', 'Lạn', 'Mink', 'Nem', 'Phúk', 'Tran'],
    'Chuyên cần': [9.0, 8.5, 7.0, 10.0, 8.0, 6.0, 9.5, 7.5, 8.0, 10.0],
    'Giữa kỳ': [8.0, 9.0, 6.5, 9.5, 7.5, 6.0, 8.5, 7.0, 7.5, 9.0],
    'Cuối kỳ': [7.5, 8.5, 6.0, 9.0, 7.0, 5.5, 8.0, 6.5, 7.0, 9.0]
}
df = pd.DataFrame(data)

# Tính điểm tổng kết (20% Chuyên cần + 30% Giữa kỳ + 50% Cuối kỳ)
df['Tong_ket'] = 0.20 * df['Chuyên cần'] + 0.30 * df['Giữa kỳ'] + 0.50 * df['Cuối kỳ']

# Định nghĩa hàm xếp loại
def xep_loai(diem):
    if diem >= 8.5:
        return 'Giỏi'
    elif diem >= 7.0:
        return 'Khá'
    elif diem >= 5.0:
        return 'Trung bình'
    else:
        return 'Yếu'

df['Xep_loai'] = df['Tong_ket'].apply(xep_loai)

# 3. Hiển thị bảng điểm
st.subheader("📋 Bảng điểm sinh viên")
st.dataframe(df, use_container_width=True)

# 4. Hiển thị thông tin thống kê
st.subheader("📊 Thống kê chung")
dtb_lop = df['Tong_ket'].mean()
sv_cao = df.loc[df['Tong_ket'].idxmax()]
sv_thap = df.loc[df['Tong_ket'].idxmin()]
so_dat = (df['Tong_ket'] >= 5.0).sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Điểm TB lớp", f"{dtb_lop:.2f}")
col2.metric("Điểm cao nhất", f"{sv_cao['Họ và tên']} ({sv_cao['Tong_ket']:.2f})")
col3.metric("Điểm thấp nhất", f"{sv_thap['Họ và tên']} ({sv_thap['Tong_ket']:.2f})")
col4.metric("Số SV đạt (>=5.0)", f"{so_dat}/10")

# 5. Danh sách chọn sinh viên (Selectbox)
st.subheader("🔍 Tra cứu chi tiết sinh viên")
selected_sv = st.selectbox("Chọn sinh viên:", df['Họ và tên'])

info_sv = df[df['Họ và tên'] == selected_sv].iloc[0]

c1, c2, c3, c4, c5 = st.columns(5)
c1.info(f"**Chuyên cần:** {info_sv['Chuyên cần']}")
c2.info(f"**Giữa kỳ:** {info_sv['Giữa kỳ']}")
c3.info(f"**Cuối kỳ:** {info_sv['Cuối kỳ']}")
c4.success(f"**Tổng kết:** {info_sv['Tong_ket']:.2f}")
c5.warning(f"**Xếp loại:** {info_sv['Xep_loai']}")

# 6. Hiển thị biểu đồ
st.subheader("📈 Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(df['Họ và tên'], df['Tong_ket'], color='#5b9bd5')
ax.set_title('Biểu đồ điểm tổng kết của 10 sinh viên')
ax.set_xlabel('Điểm tổng kết')
ax.set_ylabel('Họ và tên')
ax.set_xlim(0, 10)
ax.invert_yaxis()
st.pyplot(fig)

# 7. Thông tin người tạo (bạn nhớ sửa lại Họ tên và STT thật của mình ở đây)
st.markdown("---")
st.markdown("<p style='font-size: 13px; color: gray;'>Thực hiện bởi: Ngô Trúc Khang - STT: 19</p>", unsafe_allow_html=True)
