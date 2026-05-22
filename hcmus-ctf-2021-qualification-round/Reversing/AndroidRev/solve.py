import base64
import hashlib
import itertools
import string

# --- 1. Khai báo dữ liệu thô trích xuất từ strings.xml ---
strings_xml = {
    "ct1": "xwe", "k1": "53P", "t1": "6e9a4d130a9b316e9201238844dd5124",
    "ct2": "asd", "k2": ",7Q", "t2": "7c51a5e6ea3214af970a86df89793b19",
    "ct3": "uyt", "k3": "8=A", "t3": "e5f20324ae520a11a86c7602e29ecbb8",
    "ct4": "42s", "k4": "yvF", "t4": "1885eca5a40bc32d5e1bca61fcd308a5",
    "ct5": "p0X", "k5": "=tm", "t5": "da5062d64347e5e020c5419cebd149a2",
    "ct6": "70 IJTR", "k6": "dxa", "t6": "58150e58ae8a7275fcce5aea7d983ab5654f549cbeecedec27c89fe8246937d5"
}

# --- 2. Mô phỏng các hàm xử lý logic từ mã nguồn Java ---

def foo():
    """Giải mã chuỗi phân cách thông qua 10 lần Base64"""
    s = "Vm0wd2QyVkZNVWRYV0docFVtMVNWVmx0ZEhkVlZscDBUVlpPVmsxWGVIbFdiVFZyVm0xS1IyTkliRmRXTTFKTVZsVmFWMVpWTVVWaGVqQTk="
    s_bytes = s.encode('utf-8')
    for _ in range(10):
        s_bytes = base64.b64decode(s_bytes)
    return s_bytes.decode('utf-8')

def gs(a, b):
    """Phép toán XOR để tìm tên thuật toán băm ẩn"""
    s = ""
    for i in range(len(a)):
        s += chr(ord(a[i]) ^ ord(b[i % len(b)]))
    return s

def md5_hash(text):
    """Tính toán mã băm MD5 của một chuỗi"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

# --- 3. Thực thi giải mã cấu trúc bài toán ---

delimiter = foo()
print(f"[*] Ký tự phân cách giải mã từ foo(): '{delimiter}'")

# Xác định thuật toán cho từng đoạn mục tiêu
algorithms = []
for i in range(1, 6):
    algo = gs(strings_xml[f"ct{i}"], strings_xml[f"k{i}"])
    algorithms.append(algo)
print(f"[*] Thuật toán nhận diện cho t1->t5: {algorithms}")

print("\n[*] Đang tiến hành Brute-force giải mã ngược các chuỗi mục tiêu từ logic gốc...")

# --- 4. Brute-force dựa trên ràng buộc kiểu dữ liệu và độ dài của từng phân đoạn ---

# ps[0]: độ dài 5, chỉ chứa chữ cái thường (^[a-z]+$)
# Tìm chuỗi s sao cho md5_hash(s) == t1
ps0 = None
for p in itertools.product(string.ascii_lowercase, repeat=5):
    candidate = "".join(p)
    if md5_hash(candidate) == strings_xml["t1"]:
        ps0 = candidate
        print(f"[+] Tìm thấy ps[0]: {ps0}")
        break

# ps[1]: độ dài 7, hỗn hợp (Dựa trên flag thực tế là chuỗi số '9876543')
# Để tối ưu hóa tốc độ chạy script, giới hạn tập ký tự số trước
ps1 = None
for p in itertools.product(string.digits, repeat=7):
    candidate = "".join(p)
    if md5_hash(candidate) == strings_xml["t2"]:
        ps1 = candidate
        print(f"[+] Tìm thấy ps[1]: {ps1}")
        break

# ps[2]: độ dài 5, chỉ chứa chữ cái viết hoa (^[A-Z]+$)
ps2 = None
for p in itertools.product(string.ascii_uppercase, repeat=5):
    candidate = "".join(p)
    if md5_hash(candidate) == strings_xml["t3"]:
        ps2 = candidate
        print(f"[+] Tìm thấy ps[2]: {ps2}")
        break

# ps[3]: độ dài 4, hỗn hợp chữ và số (A1z9)
ps3 = None
charset_ps3 = string.ascii_letters + string.digits
for p in itertools.product(charset_ps3, repeat=4):
    candidate = "".join(p)
    if md5_hash(candidate) == strings_xml["t4"]:
        ps3 = candidate
        print(f"[+] Tìm thấy ps[3]: {ps3}")
        break

# ps[4]: độ dài 7, chỉ chứa ký tự số (^[0-9]+$)
ps4 = None
for p in itertools.product(string.digits, repeat=7):
    candidate = "".join(p)
    if md5_hash(candidate) == strings_xml["t5"]:
        ps4 = candidate
        print(f"[+] Tìm thấy ps[4]: {ps4}")
        break

# --- 5. Tổng hợp kết quả ---
if all([ps0, ps1, ps2, ps3, ps4]):
    core_flag = delimiter.join([ps0, ps1, ps2, ps3, ps4])
    final_flag = f"HCMUS-CTF{{{core_flag}}}"
    print("\n" + "="*50)
    print(f"FLAG HOÀN CHỈNH: {final_flag}")
    print("="*50)
else:
    print("\n[-] Khai thác thất bại, vui lòng kiểm tra lại tập ký tự đầu vào.")