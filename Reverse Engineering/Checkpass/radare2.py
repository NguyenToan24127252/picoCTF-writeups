import r2pipe

# Mở file ở chế độ debug
r2 = r2pipe.open("./checkpass", flags=["-d"])

# Phân tích hàm
r2.cmd("aa")

# Đặt breakpoint tại hàm kiểm tra mục tiêu cuối cùng
r2.cmd("db 0x00116190") 

# Chạy chương trình với input giả lập
r2.cmd("dc picoCTF{AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA}")

# Đọc giá trị thanh ghi RDI (con trỏ trỏ tới mảng kết quả)
rdi = int(r2.cmd("dr rdi"), 16)

# Dump 32 bytes kết quả dưới dạng hex
result = r2.cmd(f"pxj 32 @ {rdi}")
print(result) # Trả về mảng JSON các byte đã biến đổi