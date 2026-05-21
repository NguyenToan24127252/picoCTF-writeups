# Cho phép nhập tay string1 và string2 từ bàn phím
string1 = input("Nhập chuỗi string1 (Chìa khóa XOR): ")
string2 = input("Nhập chuỗi string2 (Dữ liệu bị XOR): ")

# Kiểm tra độ dài hai chuỗi để tránh lỗi vòng lặp
if len(string1) != len(string2):
    print("\n[!] Cảnh báo: Độ dài hai chuỗi không bằng nhau!")
    print(f"-> Độ dài string1: {len(string1)} ký tự")
    print(f"-> Độ dài string2: {len(string2)} ký tự")
    print("Vẫn tiến hành XOR dựa theo độ dài của chuỗi ngắn hơn...\n")

# Lấy độ dài của chuỗi ngắn hơn để làm mốc chạy vòng lặp (tránh lỗi IndexError)
length = min(len(string1), len(string2))

# Tiến hành XOR từng ký tự một
flag = ""
for i in range(length):
    # Lấy giá trị mã ASCII của ký tự trong string2 XOR với ký tự tương ứng trong string1
    char_xor = ord(string2[i]) ^ ord(string1[i])
    # Chuyển giá trị số sau khi XOR ngược lại thành ký tự chữ
    flag += chr(char_xor)

# In kết quả cuối cùng ra màn hình
print("-" * 30)
print("Flag của bạn là:", flag)
print("-" * 30)