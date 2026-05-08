# Đọc nội dung file enc vào biến
encoded = open('enc').read()

# Giải mã bằng cách tách từng ký tự 16-bit thành hai ký tự 8-bit
flag = ""
for c in encoded:
    # Ký tự 1 (8 bit cao): Dịch phải 8 bit
    flag += chr(ord(c) >> 8)
    # Ký tự 2 (8 bit thấp): Lấy phần dư khi chia cho 256 (hoặc dùng & 0xFF)
    flag += chr(ord(c) % 256)

print(flag)