import os
import itertools
import ctypes
from pwn import *

# 1. CẤU HÌNH & KHỞI TẠO DỮ LIỆU
context.log_level = 'error'

BINARY_PATH = './no_auth_mistery'
OUTPUT_PATH = './output'

if not os.path.exists(BINARY_PATH) or not os.path.exists(OUTPUT_PATH):
    print(f"[-] Thất bại: Thiếu file '{BINARY_PATH}' hoặc '{OUTPUT_PATH}'!")
    exit(1)

# Đọc cấu trúc file ELF bằng pwntools
elf = ELF(BINARY_PATH)
addr_index = elf.symbols['indexTable']
addr_secret = elf.symbols['secret']

# Đọc bộ đệm dữ liệu thô từ file binary
index_bytes = elf.read(addr_index, 1024)
secret_bytes = elf.read(addr_secret, 1024)

# 2. CÁC HÀM TRỢ GIÚP (HELPER FUNCTIONS)
def bytes_to_bits(byte_data: bytes) -> str:
    """Chuyển đổi chuỗi byte thành chuỗi ký tự bit liên tục (MSB-first)."""
    return "".join(f"{b:08b}" for b in byte_data)

def emul_c_encode_logic(char: str) -> int:
    """Mô phỏng chính xác thuật toán xử lý và băm ký tự của hàm encode() trong C."""
    c_lower = char.lower()
    val = ord(c_lower)
    
    # Xử lý các trường hợp đặc biệt
    if c_lower == ' ':
        val = -123  # Tương đương -0x7b
    elif '/' < c_lower < ':':
        val += 75   # Tương đương + 'K'
        
    # Ép kiểu signed char (int8) tương thích với phần cứng và trình biên dịch C
    val = ctypes.c_int8(val).value
    val -= 0x61
    val = ctypes.c_int8(val).value

    # Kiểm tra điều kiện giới hạn hợp lệ [0, 36]
    if 0 <= val <= 36:
        if val != 36: # Khác ký tự '$'
            i_var3 = ctypes.c_int((val + 18) % 36).value
            return abs(i_var3)
        return val
    return -1

# 3. DỰNG TỪ ĐIỂN GIẢI MÃ NGHỊCH ĐẢO (BIT-TO-CHAR MAP)
secret_bits = bytes_to_bits(secret_bytes)

# Phân rã indexTable thành mảng số nguyên 4-byte (Little-Endian)
index_table = [
    int.from_bytes(index_bytes[i:i+4], byteorder='little')
    for i in range(0, len(index_bytes), 4)
]

bit_to_chars = {}

# Quét bảng mã ASCII (Chỉ lọc ký tự thường, số và khoảng trắng để tránh đụng độ chữ hoa)
for i in range(256):
    char = chr(i)
    if not (char.islower() or char.isdigit() or char == ' '):
        continue  # Bỏ qua chữ HOA và ký tự rác ngay từ gốc để tránh làm dài dòng kết quả
        
    final_idx = emul_c_encode_logic(char)
    if final_idx == -1:
        continue

    # Định vị và cắt dải bit đại diện từ mảng secret
    start_bit = index_table[final_idx]
    end_bit = index_table[final_idx + 1]
    
    if start_bit < end_bit <= len(secret_bits):
        char_bits = secret_bits[start_bit:end_bit]
        bit_to_chars.setdefault(char_bits, []).append(char)

# 4. TIẾN HÀNH PHÂN RÃ FILE OUTPUT VÀ GIẢI MÃ
with open(OUTPUT_PATH, 'rb') as f:
    output_bits = bytes_to_bits(f.read())

possible_flag_layers = []
current_buffer = ""

for bit in output_bits:
    current_buffer += bit
    if current_buffer in bit_to_chars:
        possible_flag_layers.append(bit_to_chars[current_buffer])
        current_buffer = ""

# 5. XUẤT KẾT QUẢ FLAG SẠCH
print("[+] Đang giải mã khử đụng độ...")
count = 0
for chars in itertools.product(*possible_flag_layers):
    possible_flag = "".join(chars)
    print(possible_flag)
    count += 1
    if count >= 10:  # Giới hạn in tối đa vì lúc này kết quả đã cực kỳ sạch
        break