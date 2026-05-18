# 1. Đọc 26 bytes cuối cùng của file mystery.png
with open("mystery.png", "rb") as f:
    data = f.read()

# Lấy 26 bytes cuối cùng
enc_flag = bytearray(data[-26:])

# 2. Tiến hành giải mã ngược
flag = bytearray(26)

# Giai đoạn 1 & 2: Giữ nguyên (0 đến 5)
for i in range(0, 6):
    flag[i] = enc_flag[i]

# Giai đoạn 3: Trừ đi 5 (6 đến 14)
for i in range(6, 15):
    flag[i] = enc_flag[i] - 5

# Giai đoạn 4: Cộng thêm 3 (15)
flag[15] = enc_flag[15] + 3

# Giai đoạn 5: Giữ nguyên (16 đến 25)
for i in range(16, 26):
    flag[i] = enc_flag[i]

# In ra kết quả dạng string
print("Flag tìm được:", flag.decode('utf-8', errors='ignore'))