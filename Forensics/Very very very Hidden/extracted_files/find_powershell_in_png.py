#!/usr/bin/env python3
from PIL import Image

def decrypt_pico_stego(image_path):
    # Mở ảnh bằng Pillow
    with Image.open(image_path) as im:
        width, height = im.size
        pixels = im.load()
        
        print(f"[*] Kích thước ảnh: {width}x{height}")
        print("[*] Đang quét các cặp màu theo thứ tự hàng dọc/ngang chuẩn hệ thống...")
        
        # 6 tổ hợp cặp kênh màu có thể xảy ra (0:R, 1:G, 2:B)
        color_pairs = [
            (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)
        ]
        
        # THAY ĐỔI QUYẾT ĐỊNH: Duyệt Y trước (Hàng), rồi mới đến X (Cột)
        # Đây là cấu trúc lưu trữ mảng pixel chuẩn của Windows Bitmap
        for c1, c2 in color_pairs:
            extracted_bytes = bytearray()
            
            for y in range(height):
                for x in range(width):
                    p = pixels[x, y]
                    
                    # Lấy 4 bit thấp của kênh c1 dịch trái 4 vị trí làm 4 bit cao
                    # Kết hợp với 4 bit thấp của kênh c2 làm 4 bit thấp
                    byte_val = ((p[c1] & 0x0F) << 4) | (p[c2] & 0x0F)
                    extracted_bytes.append(byte_val)
            
            # Chuyển mảng byte thành chuỗi dạng văn bản đọc được
            full_text = extracted_bytes.decode('utf-8', errors='ignore')
            
            # Kiểm tra xem tổ hợp này có chứa đoạn mã PowerShell không
            if "$string1" in full_text or "$out" in full_text:
                print("\n" + "="*50)
                print(f"[+] KHỚP THÀNH CÔNG THUẬT TOÁN GỐC CỦA TOOL!")
                print(f"-> Kênh bit cao: {c1} | Kênh bit thấp: {c2}")
                print("="*50 + "\n")
                
                # Tìm vị trí đoạn script mục tiêu
                pos = full_text.find("$out")
                if pos == -1: 
                    pos = full_text.find("$string1")
                
                # In ra màn hình đoạn mã chuẩn
                print(full_text[pos:pos+1000].strip())
                
                # Ghi file ra đĩa
                with open("extracted_script.ps1", "w", encoding="utf-8") as f:
                    f.write(full_text)
                return True
                
        print("\n[-] Vẫn chưa khớp. Hãy thử đổi lại thứ tự X và Y với 6 cặp màu này.")
        return False

if __name__ == "__main__":
    decrypt_pico_stego("evil_duck.png")