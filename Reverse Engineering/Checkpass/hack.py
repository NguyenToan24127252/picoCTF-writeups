import gdb
import re
import shlex

# Toàn bộ mục tiêu cuối cùng thu được từ hàm FUN_00116190 
targets = {
    0: 0x1f, 1: 0x01, 2: 0x50, 3: 0x99, 4: 0xb8, 5: 0x22, 6: 0x3a, 7: 0xcb,
    8: 0x0d, 9: 0xcb, 10: 0xae, 11: 0xcb, 12: 0xd9, 13: 0x20, 14: 0x3a, 15: 0x48,
    16: 0x05, 17: 0x7b, 18: 0x7b, 19: 0xcf, 20: 0xcd, 21: 0x68, 22: 0x46, 23: 0xd3,
    24: 0xcf, 25: 0xe6, 26: 0xcd, 27: 0x22, 28: 0xf9, 29: 0x3a, 30: 0x05, 31: 0x7b
}

class FlagSolver(gdb.Command):
    def __init__(self):
        super(FlagSolver, self).__init__("solve_flag", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        flag_result = ["?"] * 32
        
        # ĐẶT BREAKPOINT TẠI HÀM CHECK CUỐI CÙNG (Đã chạy xong 4 vòng mã hóa) [cite: 169-170, 181-185]
        check_func_addr = "*0x55555556a190"
        
        # Duyệt từng vị trí ký tự flag
        for position in range(32):
            print(f"[*] Đang dò tìm ký tự tại vị trí {position}...")
            
            # Thử các ký tự ASCII khả kiến từ 32 đến 126
            for char_code in range(32, 127):
                payload = ["A"] * 32
                payload[position] = chr(char_code)
                payload_str = "".join(payload)
                
                full_flag = f"picoCTF{{{payload_str}}}"
                safe_argument = shlex.quote(full_flag)
                
                try:
                    # Khởi động và đặt bẫy chặn cửa hàm check 
                    gdb.execute(f"starti {safe_argument}", to_string=True)
                    gdb.execute(f"break {check_func_addr}", to_string=True)
                    
                    # Chỉ cần continue ĐÚNG 1 LẦN duy nhất để đến thẳng hàm check 
                    gdb.execute("continue", to_string=True)
                        
                    # Lúc này trong hàm check, RDI chính là param_1 chứa mảng 32 bytes kết quả sạch [cite: 169, 181-183]
                    # Không còn cấu trúc Fat Pointer lằng nhằng nữa vì đây là mảng local_50 phẳng [cite: 169, 181-183]
                    rdi_val = gdb.parse_and_eval("$rdi")
                    gdb_output = gdb.execute(f"x/32xb {rdi_val}", to_string=True)
                    hex_bytes = re.findall(r"0x[0-9a-fA-F]{2}", gdb_output)
                    
                    if len(hex_bytes) >= 32:
                        current_encrypted_byte = int(hex_bytes[position], 16)
                        
                        # So khớp trực tiếp tuyến tính 1:1 
                        if current_encrypted_byte == targets[position]:
                            flag_result[position] = chr(char_code)
                            print(f"[+] Tìm thấy ký tự thứ {position}: '{chr(char_code)}'")
                            break
                except Exception as e:
                    pass
                finally:
                    gdb.execute("delete", to_string=True)
                        
            print(f"-> Flag hiện tại: picoCTF{{{''.join(flag_result)}}}")

FlagSolver()