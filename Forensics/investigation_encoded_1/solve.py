import os
from pwn import *

# Cấu hình log của pwntools cho đỡ hiện thông báo thừa
context.log_level = 'error'

# 1. Tải file thực thi và đọc dữ liệu tự động
if not os.path.exists('./mystery') or not os.path.exists('./output'):
    print("[-] Vui lòng để file 'mystery' và 'output' cùng thư mục với script này!")
    exit(1)

elf = ELF('./mystery')

# Lấy địa chỉ của matrix và secret
addr_matrix = elf.symbols['matrix']
addr_secret = elf.symbols['secret']

# Đọc toàn bộ dữ liệu thô (Ước lượng độ dài an toàn)
# Matrix: 30 ký tự (a-z, {, }, _, vv) * 8 byte = 240 bytes
matrix_bytes = elf.read(addr_matrix, 256)
# Secret: Đọc khoảng 100 bytes dữ liệu bit
secret_bytes = elf.read(addr_secret, 128)

# 2. Hàm chuyển đổi một chuỗi bytes thành chuỗi bit liên tục (MSB-first)
def bytes_to_bits(byte_data):
    return "".join(f"{b:08b}" for b in byte_data)

secret_bits = bytes_to_bits(secret_bytes)

# 3. Xây dựng bảng từ điển để giải mã (Chuỗi bit -> Ký tự)
bit_to_char = {}

# Duyệt qua các ký tự từ 'a' đến '{' như trong hàm encode() của C
# 'a' là 0x61, '{' là 0x7b (ký tự đại diện cho khoảng trắng ' ')
for i in range(0x61, 0x7b + 1):
    char_idx = i - 0x61
    # Mỗi phần tử matrix gồm 2 biến int (4-byte), tổng cộng 8-byte
    offset = char_idx * 8
    
    # Đọc cấu trúc matrix: int thứ nhất là length, int thứ hai là start_index
    length = int.from_bytes(matrix_bytes[offset:offset+4], byteorder='little')
    start_idx = int.from_bytes(matrix_bytes[offset+4:offset+8], byteorder='little')
    
    # Cắt chuỗi bit tương ứng từ mảng secret
    char_bits = secret_bits[start_idx : start_idx + length]
    
    # Xác định ký tự thực tế (nếu là '{' thì đổi lại thành khoảng trắng ' ')
    actual_char = ' ' if chr(i) == '{' else chr(i)
    
    # Lưu vào từ điển giải mã
    bit_to_char[char_bits] = actual_char

# Thêm thủ công các ký tự đặc biệt thường có trong flag nếu thuật toán isValid cho phép
# (Thông thường picoCTF sẽ có thêm dấu gạch dưới '_', ngoặc nhọn '}' nếu chúng nằm ngoài bảng a-z)
# Script này dựa trên việc giải mã từ bộ từ điển đã được tính toán từ matrix

# 4. Đọc file bằng chứng 'output' và chuyển thành chuỗi bit
with open('output', 'rb') as f:
    output_bytes = f.read()

output_bits = bytes_to_bits(output_bytes)

# 5. Giải mã chuỗi bit của file output để tìm flag
flag = ""
current_buffer = ""

for bit in output_bits:
    current_buffer += bit
    if current_buffer in bit_to_char:
        flag += bit_to_char[current_buffer]
        current_buffer = "" # Xóa bộ đệm sau khi khớp ký tự

print("[+] Kết quả giải mã:")
print(flag)