### Bài toán
- Description
    - Can you get the flag?
Reverse engineer this binary.

### Giải
## 1. Giám định tệp tin (Reconnaissance)

Đầu tiên, chúng ta kiểm tra các lớp bảo vệ của tệp thực thi bằng công cụ `checksec`:

```bash
checksec --file=keygenme
```

**Kết quả:**

* **RELRO:** Full RELRO (Không thể ghi đè bảng GOT).
* **Stack:** Canary found (Có chống tràn stack).
* **NX:** NX enabled (Không thể thực thi mã trên stack).
* **PIE:** PIE enabled (Địa chỉ hàm thay đổi mỗi khi chạy).
* **Symbols:** **No Symbols** (Tệp đã bị stripped, không còn tên hàm gốc).

---

## 2. Phân tích tĩnh với Ghidra 

Vì tệp đã bị xóa Symbol, ta sử dụng **Ghidra** để dịch ngược mã máy thành mã C.

### Bước 1: Tìm hàm Main thực sự

Mở hàm `entry`, ta thấy hàm này gọi `__libc_start_main`. Tham số đầu tiên truyền vào chính là hàm Logic chính (Main):

```c
__libc_start_main(FUN_0010148b, param_2, ...);

```

=> Truy cập vào **`FUN_0010148b`**.

### Bước 2: Phân tích hàm Logic chính

Tại `FUN_0010148b`, chương trình thực hiện:

* `printf("Enter your license key: ");`
* `fgets(local_38, 0x25, stdin);`: Nhận đầu vào 37 ký tự.
* `cVar1 = FUN_00101209(local_38);`: Truyền key vào hàm kiểm tra.

---

## 3. Giải mã thuật toán kiểm tra (Deep Dive)

Truy cập vào hàm **`FUN_00101209`**, đây là nơi Flag được lắp ráp.

### Cấu trúc Flag (`auStack_38`):

1. **Phần đầu (Static):** `builtin_memcpy(local_98, "picoCTF{br1ng_y0ur_0wn_k3y_", 0x1c);` (28 ký tự đầu).
2. **Phần đuôi (Static):** `local_ba[0] = '}';`
3. **Phần động (Dynamic):** Chương trình tính **MD5** của phần đầu Flag và lưu vào chuỗi Hex `local_78`. Sau đó, nó "nhặt" các ký tự từ bộ nhớ stack để điền vào phần còn thiếu.

### Kỹ thuật truy vết Stack Offset:

Dựa vào khoảng cách địa chỉ giữa mảng MD5 (`local_78` tại `-0x78`) và các biến đơn lẻ, ta xác định được vị trí của chúng trong chuỗi MD5:

* **local_6b:** `0x78 - 0x6b = 13` => Index 13.
* **local_6a:** `0x78 - 0x6a = 14` => Index 14.
* **local_66:** `0x78 - 0x66 = 18` => Index 18.
* **local_60:** `0x78 - 0x60 = 24` => Index 24.
* **local_5e:** `0x78 - 0x5e = 26` => Index 26.
* **local_5b:** `0x78 - 0x5b = 29` => Index 29.

**Thứ tự lắp ráp vào Flag:**

| Vị trí Flag | Biến nguồn | Vị trí trong chuỗi MD5 |
| --- | --- | --- |
| Index 28 | `local_6b` | **13** |
| Index 29 | `local_66` | **18** |
| Index 30 | `local_5b` | **29** |
| Index 31 | `local_78[1]` | **1** |
| Index 32 | `local_6a` | **14** |
| Index 33 | `local_60` | **24** |
| Index 34 | `local_5e` | **26** |
| Index 35 | `local_5b` | **29** |

---

## 4. Script giải mã (Solution)

Sử dụng Python để tái tạo lại thuật toán MD5 và lấy đúng các ký tự theo Offset đã phân tích:

```python
import hashlib

# 1. Phần đầu cố định
prefix = "picoCTF{br1ng_y0ur_0wn_k3y_"

# 2. Tính MD5 của phần đầu
md5_hex = hashlib.md5(prefix.encode()).hexdigest()

# 3. Lắp ráp phần động theo đúng thứ tự logic của Ghidra
# Thứ tự index: 13, 18, 29, 1, 14, 24, 26, 29
dynamic = (md5_hex[13] + md5_hex[18] + md5_hex[29] + md5_hex[1] + 
           md5_hex[14] + md5_hex[24] + md5_hex[26] + md5_hex[29])

# 4. Kết quả cuối cùng
flag = prefix + dynamic + "}"
print(f"FLAG: {flag}")

```

**FLAG:** `picoCTF{br1ng_y0ur_0wn_k3y_xxxxxxxx}` *(Thay xxxxxxxx bằng kết quả chạy script)*.

### Note
- **Kiến thức vận dụng:** Cách tổ chức bộ nhớ Stack của biến cục bộ trong C, thuật toán băm (MD5), và kỹ thuật đọc XREFs trong Ghidra.
- **Bài học:** Ngay cả khi tệp đã bị **stripped**, việc dựa vào các chuỗi hằng số (Strings) và các hàm thư viện (như `sprintf`, `MD5`) vẫn giúp chúng ta định vị được logic cốt lõi.