### Bài toán
- Description
    - A new modular challenge!
Download the message here.
Take each number mod 41 and find the modular inverse for the result. Then map to the following character set: 1-26 are the alphabet, 27-36 are the decimal digits, and 37 is an underscore.
Wrap your decrypted message in the picoCTF flag format (i.e. picoCTF{decrypted_message})

### Giải
- B1: Tính x = n (mod 41)
- B2: tìm inv = x^-1 (mod 41) (sử dụng hàm pow trong python)
- Ánh xạ: 1...26 -> A...Z ; 27...36->0...9 ; 37->_(underscore)
- python:
```
def map_char(n):
    if 1 <= n <= 26:
        return chr(ord('A') + n - 1)
    elif 27 <= n <= 36:
        return chr(ord('0') + n - 27)
    elif n == 37:
        return '_'
    return '?'

# Đọc dữ liệu trực tiếp từ file message.txt
try:
    with open('message.txt', 'r') as f:
        # Tách các số dựa trên khoảng trắng và chuyển sang kiểu int
        numbers = [int(x) for x in f.read().split()]
    
    decrypted = ""
    for num in numbers:
        # Bước 1: Mod 41
        x = num % 41
        
        # Bước 2: Tìm nghịch đảo modulo 41
        # Sử dụng pow(x, -1, 41) - cực kỳ nhanh và chuẩn
        try:
            inv = pow(x, -1, 41)
            # Bước 3: Ánh xạ sang ký tự
            decrypted += map_char(inv)
        except ValueError:
            # Nếu x không có nghịch đảo (ví dụ x=0)
            decrypted += '?'

    print(f"picoCTF{{{decrypted}}}")

except FileNotFoundError:
    print("Lỗi: Không tìm thấy file message.txt trong thư mục này!")
```