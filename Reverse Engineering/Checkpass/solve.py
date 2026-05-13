from z3 import *

# 1. Khai báo
input_chars = [BitVec(f'p_{i}', 8) for i in range(32)]
solver = Solver()

for p in input_chars:
    solver.add(p >= 32, p <= 126)

# 2. Đọc dữ liệu (Đảm bảo File Offset chính xác)
try:
    with open("checkpass", "rb") as f:
        f.seek(0x86f0) # Kiểm tra lại offset này trong Ghidra Listing view
        sbox_data = list(f.read(1024))
        f.seek(0x9600)
        perm_raw = list(f.read(1024))
except:
    print("Lỗi đọc file!")
    exit()

# Nạp S-box vào danh sách hằng số Z3 để solver tra cứu
# [cite: 407-417, 449]
sbox_const = [BitVecVal(b, 8) for b in sbox_data]

def get_perm_idx(round_num, i):
    # Mỗi index là ulong (8 bytes) [cite: 140-149]
    offset = (round_num * 32 + i) * 8
    return perm_raw[offset]

# 3. Mô phỏng hàm xử lý [cite: 460-461]
def sub_54E0(data, round_num):
    # Bước 1: Substitution (Thay thế từng byte)
    box_no = round_num * 256
    # Tra cứu giá trị thực từ sbox_const thay vì dùng Array/Select mơ hồ
    tmp = []
    for d in data:
        # Tạo bảng tra cứu (Lookup table) cho Z3
        # Đây là cách "ép" Z3 dùng đúng dữ liệu S-box bạn đã đọc
        lookup = [If(d == j, sbox_const[box_no + j], BitVecVal(0, 8)) for j in range(256)]
        # Kết hợp các điều kiện If thành một biểu thức duy nhất cho 1 byte
        res = BitVecVal(0, 8)
        for val in lookup:
            res = res | val
        tmp.append(res)
    
    # Bước 2: Permutation (Đổi chỗ) [cite: 418-448]
    output = [None] * 32
    for i in range(32):
        src_idx = get_perm_idx(round_num, i)
        output[i] = tmp[src_idx]
    return output

# 4. Thực thi 4 vòng [cite: 403-405]
state = input_chars
for r in range(4):
    state = sub_54E0(state, r)

# 5. Khớp mục tiêu [cite: 450-458, 461]
targets = {
    25: 0xe6, 0: 0x1f, 14: 0x3a, 19: 0xcf, 23: 0xd3, 1: 0x01, 29: 0x3a, 27: 0x22,
    26: 0xcd, 12: 0xd9, 31: 0x7b, 6: 0x3a, 10: 0xae, 15: 0x48, 30: 0x05, 7: 0xcb,
    11: 0xcb, 5: 0x22, 22: 0x46, 16: 0x05, 21: 0x68, 3: 0x99, 20: 0xcd, 8: 0x0d,
    28: 0xf9, 13: 0x20, 17: 0x7b, 2: 0x50, 9: 0xcb, 4: 0xb8, 24: 0xcf, 18: 0x7b
}

for idx, val in targets.items():
    solver.add(state[idx] == val)

# 6. Kết quả
print("[*] Đang giải...")
if solver.check() == sat:
    m = solver.model()
    flag = "".join([chr(m[p].as_long()) for p in input_chars])
    print(f"\n[+] FLAG TÌM THẤY: picoCTF{{{flag}}}")
else:
    print("\n[-] Unsat. Hãy kiểm tra lại File Offset 0x86f0 trong Ghidra!")