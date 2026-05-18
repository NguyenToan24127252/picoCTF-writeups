# 1. Đọc dữ liệu từ 3 file
with open("mystery.png", "rb") as f:
    m1_all = f.read()
with open("mystery2.png", "rb") as f:
    m2_all = f.read()
with open("mystery3.png", "rb") as f:
    m3_all = f.read()

# Trích xuất số lượng byte tương ứng ở cuối mỗi file
m1 = m1_all[-16:]
m2 = m2_all[-2:]
m3 = m3_all[-8:]

# Khởi tạo mảng chứa flag gồm 26 phần tử
flag = [0] * 26

# 2. Khôi phục theo bản đồ cấu trúc
flag[0] = m2[0] - 0x15
flag[1] = m3[0]
flag[2] = m3[1]
flag[3] = m2[1] - 4
flag[4] = m1[0]
flag[5] = m3[2]

# flag[6] đến flag[9] lấy từ m1[1:5]
for i in range(6, 10):
    flag[i] = m1[i - 5] # i-5 tương ứng dịch từ index 1 đến 4

# flag[10] đến flag[14] lấy từ m3[3:8]
for i in range(10, 15):
    flag[i] = m3[i - 7] # i-7 tương ứng dịch từ index 3 đến 7

# flag[15] đến flag[25] lấy từ m1[5:16]
for i in range(15, 26):
    flag[i] = m1[i - 10] # i-10 tương ứng dịch từ index 5 đến 15

# 3. Chuyển đổi mảng số thành chuỗi ký tự và in ra
flag_str = "".join([chr(b & 0xFF) for b in flag])
print("Flag tìm được là:", flag_str)