#!/usr/bin/env python3
import angr
import claripy
import logging

# Tắt các log cảnh báo rác của angr để màn hình sạch sẽ
logging.getLogger('angr').setLevel(logging.CRITICAL)

# 1. Khởi tạo dự án angr với file checkpass
project = angr.Project("./checkpass", auto_load_libs=False)

print("[*] Đang khởi tạo các biến toán học bằng claripy...")
# 2. Tạo mảng biến symbolic cho flag (32 ký tự nằm trong picoCTF{...} -> tổng là 41 ký tự)
flag_chars = [claripy.BVS(f"flag_{i}", 8) for i in range(41)]

# Sử dụng claripy.Concat để nối các byte đơn lẻ thành một chuỗi bit-vector duy nhất
argv1 = claripy.Concat(*flag_chars)

# 3. Tạo trạng thái ban đầu với đối số argv chuẩn chứa biến symbolic
initial_state = project.factory.entry_state(args=["./checkpass", argv1])

# Ràng buộc điều kiện: Các ký tự bên trong phải là ký tự ASCII in được (từ 32 đến 126)
for i in range(41):
    initial_state.solver.add(flag_chars[i] >= 32)
    initial_state.solver.add(flag_chars[i] <= 126)

# 4. Kích hoạt bộ mô phỏng càn quét bộ nhớ
simulation = project.factory.simulation_manager(initial_state)

print("[*] CHIẾN THUẬT MỚI: Ép 'angr' quét thẳng theo địa chỉ hàm check...")

# Lấy Base Address ảo mà angr tự động map cho file (thường là 0x400000)
base_addr = project.loader.main_object.mapped_base

# ĐỊA CHỈ PHÓNG THẲNG: Điểm kết thúc hàm check cuối cùng khi pass qua hết 32 ký tự
# Offset tĩnh trong Ghidra của lệnh nhảy thành công là 0x162d0
success_address = base_addr + 0x162d0

# ĐỊA CHỈ NÉ TRÁNH: Điểm nhảy tới thông báo "Invalid password"
# Offset tĩnh trong Ghidra của nhánh báo sai pass là 0x162f0
avoid_address = base_addr + 0x162f0

# 5. Ra lệnh cho angr quét mục tiêu theo địa chỉ cứng
simulation.explore(find=success_address, avoid=avoid_address)

# 6. Bung kết quả
if simulation.found:
    solution_state = simulation.found[0]
    result_flag = solution_state.solver.eval(argv1, cast_to=bytes)
    print("\n[+] TÌM THẤY FLAG CHUẨN XỊN 100%:")
    print(result_flag.decode('utf-8'))
else:
    print("[-] Không tìm thấy đường đi thỏa mãn địa chỉ chỉ định.")