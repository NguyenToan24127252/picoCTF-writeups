# Bài toán
- Description
    - What is the password?
Flag format: picoCTF{...}
File: checkpass

# Giải
## Phân tích = Ghidra
- Ta không thấy hàm main => File đã bị xóa ký hiệu (Stripped Binary)
- Dựa vào hàm entry và FUN_00116c60, chương trình bắt đầu tại FUN_00115a20. Đây là nơi xử lý logic nhập liệu và kiểm tra flag.
- Trong hàm FUN_00115a20, ta phân tích:
```
if ((*plVar7 == 0x7b4654436f636970) && ((char)plVar7[5] == '}')) {
    if ((char)plVar7[1] < -0x40) { // Kiểm tra độ dài/loại dữ liệu
        // ...
    }
}
```
- Kinh nghiệm nhận biết: * Giá trị 0x7b4654436f636970 khi đổi sang ASCII (Little Endian) chính là picoCTF{
    - Phép so sánh với } ở cuối xác nhận đây là bước kiểm tra khung của flag
    - Con số 0x29 (41 decimal) xuất hiện trong các hàm liên quan (FUN_00154290) cho biết tổng độ dài chuỗi là 41 ký tự
- Sau khi đã xác định được chuỗi nhập vào đúng format, chương trình sẽ "xào nấu" nó qua hàm:
```
FUN_001166f0(local_50, &local_f8);
```
- Kinh nghiệm nhận biết: * Hàm này nhận vào local_f8 (địa chỉ chứa flag nhập) và trả kết quả vào local_50 (một vùng đệm tạm thời)
    - Trong Reverse Engineering, hễ thấy một hàm nhận input từ người dùng rồi trả ra một mảng mới ngay trước khi so sánh, thì đó chắc chắn là Hàm Mã Hóa/Biến Đổi.
- Đoạn mã kiểm tra kết quả:
```
cVar6 = FUN_00116190(local_50);
if (cVar6 == '\0') {
    FUN_001159e0(); // Thường là hàm in ra "Wrong Password"
}
else {
    FUN_00116750(); // Thường là hàm in ra "Correct! Here is your flag"
}
```
- Kinh nghiệm nhận biết: * cVar6 nhận giá trị trả về từ FUN_00116190 (một hàm kiểu boolean - đúng/sai).  
    - Nếu ta nhìn vào FUN_00116190, ta sẽ thấy hàng loạt phép so sánh == với các giá trị hex lạ lùng (0x1f, 0xe6, 0x3a...). Đó chính là các Target Values (giá trị đích) mà flag sau khi mã hóa phải đạt được .  
- Mở hàm FUN_001166f0 thấy hàm gọi hàm biến đổi lõi FUN_00116790 đúng 4 lần liên tiếp. Mỗi lần gọi đại diện cho một "Round" (vòng mã hóa):  
    - Vòng 0: Nhận dữ liệu gốc (param_2) và lưu kết quả vào mảng tạm auStack_78.  
    - Vòng 1: Lấy kết quả từ Vòng 0 làm đầu vào và lưu vào local_58.  
    - Vòng 2: Lấy kết quả từ Vòng 1 làm đầu vào và lưu vào local_38.  
    - Vòng 3: Lấy kết quả từ Vòng 2 làm đầu vào và lưu vào param_1 (đây là kết quả cuối cùng trả về cho hàm main).
- Phân tích hàm FUN_00116790 thấy đây là người trực tiếp thực hiện việc thay đổi các ký tự flag của ta qua hai công đoạn chính: Substitution (Thay thế) và Permutation (Hoán vị):
    - Vào: Mảng 32 byte (flag).
    - Bước 1: Thay đổi giá trị từng byte qua bảng tra cứu (S-Box) .  
    - Bước 2: Đổi chỗ các byte đó cho nhau theo quy luật (Permutation) .  
    - Ra: Mảng 32 byte đã bị xáo trộn, sẵn sàng cho vòng tiếp theo hoặc so sánh cuối cùng.
    - Phân tích mã thì ta thấy:
    1. Nhận diện bảng S-box (Substitution)
    - Trong hàm FUN_00116790, mình nhìn vào dòng này:param_2[0x1d] = (&DAT_001086f0)[(ulong)param_2[0x1d] + param_3];   
    - Dấu hiệu 1 (Ký hiệu &DAT_...): Trong Ghidra, khi ta thấy một biến bắt đầu bằng &DAT_, đó là một con trỏ trỏ vào vùng dữ liệu tĩnh (Data Segment) của file.  
    - Dấu hiệu 2 (Cấu trúc mảng): Phép toán [index] cho thấy chương trình đang truy cập mảng. - Việc lấy giá trị byte nhập vào (param_2[0x1d]) làm chỉ số index là đặc điểm nhận dạng 100% của một S-box (Bảng thay thế) .  
    - Dấu hiệu 3 (Địa chỉ gốc): Con số 001086f0 chính là địa chỉ ảo. Trong các file ELF 64-bit đơn giản, phần 10 ở đầu thường là địa chỉ base, phần 86f0 phía sau chính là File Offset (vị trí trong file thực tế).
    2. Nhận diện bảng Hoán vị (Permutation)
    - Tiếp tục quan sát phần dưới của hàm, nơi có các lệnh logic lồng nhau: uVar2 = *(ulong *)(&DAT_00109640 + param_3);   
    - Dấu hiệu 1 (Kiểu dữ liệu ulong *): Chương trình ép kiểu vùng dữ liệu đó thành ulong (8 byte). Điều này giải thích tại sao trong file solve.py của ta, mỗi bước nhảy index lại nhân với 8.  
    - Dấu hiệu 2 (Sự liên tục): Ghidra liệt kê một loạt địa chỉ như 00109640, 001096c8, 00109600 . Khi mình thấy các địa chỉ này cụm lại gần nhau (quanh vùng 0x9600), mình biết ngay đây là một Ma trận Hoán vị khổng lồ.  
    - Dấu hiệu 3 (Dùng làm vị trí): Biến uVar2 sau khi lấy ra từ địa chỉ này được dùng để lấy dữ liệu từ mảng tạm: *(undefined1 *)((long)&local_28 + uVar2). Nếu uVar2 được dùng để chọn vị trí lấy byte, thì bảng chứa uVar2 chắc chắn là bảng hoán vị.

## Giải = z3-solver
Dưới đây là bản Write-up chi tiết về cách hoạt động của script giải mã, đối chiếu trực tiếp giữa mã nguồn Python và các thành phần ta đã trích xuất từ Ghidra.

### 1. Tổng quan thuật toán
Chương trình thực hiện kiểm tra flag theo cấu trúc **SP-Network** (Substitution-Permutation Network) gồm **4 vòng (rounds)**.
* **Input:** Một chuỗi dài 32 ký tự nằm trong định dạng `picoCTF{...}`.
* **Xử lý:** Mỗi vòng gồm bước thay thế giá trị (Substitution) qua S-box và đổi chỗ (Permutation).
* **Output:** Sau 4 vòng, kết quả được so sánh với một bảng giá trị cố định.

---

### 2. Phân tích chi tiết Script Giải (`solve.py`)

#### Bước 1: Khai báo biến với Z3

```python
input_chars = [BitVec(f'p_{i}', 8) for i in range(32)]
solver = Solver()
for p in input_chars:
    solver.add(p >= 32, p <= 126)

```

* **Nguồn gốc:** Trích xuất từ hàm `FUN_00115a20`.
* **Giải thích:** Chương trình yêu cầu nhập vào một chuỗi, sau đó lấy ra 32 ký tự bên trong dấu ngoặc nhọn. Vì là flag, các ký tự này phải nằm trong khoảng ASCII in được (từ 32 đến 126).

#### Bước 2: Trích xuất dữ liệu tĩnh (S-box & Permutation)

```python
with open("checkpass", "rb") as f:
    f.seek(0x86f0) 
    sbox_data = list(f.read(1024))
    f.seek(0x9600)
    perm_raw = list(f.read(1024))

```
* **Nguồn gốc:** Lấy từ địa chỉ `DAT_001086f0` và `DAT_00109600` trong Ghidra.
* **Giải thích:** * **0x86f0:** Chứa bảng thay thế (S-box). Mỗi vòng dùng 256 byte, 4 vòng là 1024 byte.
* **0x9600:** Chứa bảng hoán vị. Mỗi vị trí được lưu dưới dạng `ulong` (8 bytes).

#### Bước 3: Hàm mô phỏng biến đổi (`sub_54E0`)

Hàm này mô phỏng lại toàn bộ logic của `FUN_00116790`.

**A. Substitution (Thay thế):**

```python
lookup = [If(d == j, sbox_const[box_no + j], BitVecVal(0, 8)) for j in range(256)]

```
* **Nguồn gốc:** Dòng code `param_2[i] = (&DAT_001086f0)[(ulong)param_2[i] + param_3];`.
* **Hoạt động:** Lấy giá trị của byte hiện tại làm chỉ số để tra cứu giá trị mới trong bảng S-box tại `0x86f0`.

**B. Permutation (Hoán vị):**

```python
def get_perm_idx(round_num, i):
    offset = (round_num * 32 + i) * 8
    return perm_raw[offset]

```
* **Nguồn gốc:** Các địa chỉ `DAT_00109600` đến `DAT_001096f8` trong file txt.
* **Hoạt động:** Lấy byte tại vị trí được chỉ định bởi bảng hoán vị. Vì mỗi index trong file gốc chiếm 8 byte (ulong), nên script phải nhân `offset` với 8 để lấy đúng byte giá trị.
#### Bước 4: Thiết lập mục tiêu (Targets)

```python
targets = { 25: 0xe6, 0: 0x1f, ... }

```
* **Nguồn gốc:** Trích xuất từ hàm so sánh cuối cùng **`FUN_00116190`**.
* **Giải thích:** Đây là kết quả "chuẩn" mà chương trình mong đợi. Ví dụ: `param_1[0x19] == -0x1a` trong Ghidra tương ứng với vị trí 25 có giá trị `0xe6` ($256 - 26 = 230$).
---

### 3. Quy trình thực thi của Z3

1. **Khởi tạo:** Z3 tạo ra 32 biến chưa biết.
2. **Mô phỏng:** Script bắt Z3 đi qua 4 vòng tính toán y hệt như chương trình gốc: `Substitute` $\rightarrow$ `Permute`.
3. **Ràng buộc:** Sau 4 vòng, kết quả tại mỗi vị trí phải khớp với từ điển `targets`.
4. **Giải mã:** Z3 sử dụng thuật toán giải hệ phương trình để tìm ngược lại 32 giá trị ban đầu thỏa mãn mọi điều kiện trên.

**Kết quả:** Khi chạy lệnh `solver.check()`, nếu tìm thấy kết quả (`sat`), script sẽ in ra flag có dạng `picoCTF{...}`. ->Nhưng mà flag vẫn còn sai sẽ làm tiếp trong tương lai :(((((

# Note
### 1. Dấu hiệu nhận biết thuật toán (Pattern Recognition)
* **Cấu trúc SP-Network:** Khi thấy một hàm thực hiện đồng thời việc thay đổi giá trị byte (**Substitution**) và thay đổi vị trí byte (**Permutation**) lặp lại nhiều vòng, đây là cấu trúc của một hệ mã hóa khối (Block Cipher). 
* **Unrolled Loops:** Thay vì dùng vòng lặp `for`, lập trình viên (hoặc trình biên dịch) có thể viết trải dài các lệnh gọi hàm (như cách gọi `FUN_00116790` 4 lần). Đừng để việc thiếu vòng lặp làm ta bối rối. 
### 2. Kỹ thuật "Soi" địa chỉ dữ liệu trong Ghidra
* **Base Address vs. File Offset:** Địa chỉ ảo trong Ghidra (ví dụ `0x001086f0`) thường bao gồm một Base Address (thường là `0x100000` cho ELF 64-bit). Để lấy dữ liệu bằng Python `f.seek()`, ta cần tính toán File Offset bằng cách lấy `Virtual Address - Base Address` (ví dụ: `0x86f0`).
* **Ký hiệu `&DAT_`:** Đây là chỉ dấu cho thấy chương trình đang truy cập vào một mảng dữ liệu tĩnh (S-box, Permutation Table, Key...). Luôn bắt đầu từ các địa chỉ này để tìm "nguyên liệu" giải mã.
### 3. Phân tích các con số "Biết nói"
* **`0x7b4654436f636970`:** Đây là hằng số cực kỳ phổ biến trong picoCTF, tương đương với chuỗi `picoCTF{` khi đọc theo thứ tự Little Endian. Bổ sung: HCMUS-CT -> 0x54432d53554d4348 ; HCMUS_CT -> 0x54435f53554d4348 ; HCMUSCTF -> 0x46544353554d4348
* **`0x100` (256 decimal):** Thường dùng làm offset cho S-box vì mỗi bảng S-box chuẩn có 256 phần tử. 
* **`0x20` (32 decimal):** Độ dài của phần nội dung Flag cần tìm. Mọi bảng hoán vị hoặc mảng dữ liệu dài 32 đơn vị đều xoay quanh con số này. 
### 4. Lưu ý khi trích xuất Target Values
* **Xử lý số âm (Signed vs. Unsigned):** Ghidra đôi khi hiển thị giá trị dạng số âm (ví dụ `-0x1a`). ta phải chuyển nó về dạng Unsigned 8-bit bằng công thức: `256 - abs(value)` (ví dụ: $256 - 26 = 230$ hay `0xe6`) để nạp vào Python chính xác. 
### 5. Tại sao dùng Z3-Solver?
* **Lợi thế:** Thay vì phải viết code giải ngược (Inverse Function) cho từng bước Substitution và Permutation cực kỳ phức tạp và dễ sai sót, Z3 cho phép ta chỉ cần "mô tả lại" (Model) thuật toán xuôi và để máy tính tự tìm ngược lại kết quả.
* **Độ chính xác:** Z3 đảm bảo tìm ra đúng giá trị trong không gian 32 byte mà không cần ta phải hiểu sâu về toán học đảo ngược ma trận hoán vị.
