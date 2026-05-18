# Bài toán
- Description
    - What can you make of this?
We have recovered a binary and 1 file: image01. See what you can make of it. NOTE: The flag is not in the normal picoCTF{XXX} format.

# Giải
- Ta cứ tiếp tục analyze = ghidra như bài investigation_encoded_1 và thấy hàm main cũng hoạt động tương tự -> ta mở hàm encode()
```
void encode(void)

{
  byte bVar1;
  undefined4 uVar2;
  int iVar3;
  int local_10;
  char local_9;
  
  while (*flag_index < flag_size) {
    local_9 = lower((int)*(char *)(*flag_index + flag));
    if (local_9 == ' ') {
      local_9 = -0x7b;
    }
    else if (('/' < local_9) && (local_9 < ':')) {
      local_9 = local_9 + 'K';
    }
    local_9 = local_9 + -0x61;
    if ((local_9 < '\0') || ('$' < local_9)) {
      badChars = 1;
    }
    if (local_9 != '$') {
      iVar3 = (local_9 + 0x12) % 0x24;
      bVar1 = (byte)(iVar3 >> 0x1f);
      local_9 = ((byte)iVar3 ^ bVar1) - bVar1;
    }
    iVar3 = *(int *)(indexTable + (long)(local_9 + 1) * 4);
    for (local_10 = *(int *)(indexTable + (long)(int)local_9 * 4); local_10 < iVar3;
        local_10 = local_10 + 1) {
      uVar2 = getValue(local_10);
      save(uVar2);
    }
    *flag_index = *flag_index + 1;
  }
  while (remain != 7) {
    save(0);
  }
  return;
}
```
### Phân tích hàm `encode()` 

Vẫn là thuật toán mã hóa dạng Bit-stream (nhìn đoạn lặp gọi `getValue(local_10)` và `save(uVar2)` là ta biết ngay). Tuy nhiên, trước khi đi tra bảng để lấy bit, ký tự đã bị **băm vằn vện** qua một loạt phép toán.

#### 1. Chuẩn hóa và "Chuyển hệ" ký tự

```c
local_9 = lower((int)*(char *)(*flag_index + flag));
if (local_9 == ' ') {
  local_9 = -0x7b; // Đổi khoảng trắng thành -123 (tức là 0x85)
}
else if (('/' < local_9) && (local_9 < ':')) {
  local_9 = local_9 + 'K'; // Ký tự từ '0' đến '9' (ASCII 48 - 57) sẽ được cộng thêm 75 ('K')
}
local_9 = local_9 + -0x61; // Trừ đi 'a' (0x61)
```

* Đoạn này biến đổi ký tự thành một chỉ số (index) tạm thời `local_9`.
* Nếu `local_9` nằm ngoài khoảng từ `0` đến `36` (`'$'` chính là `0x24` = 36 trong hệ thập phân), chương trình sẽ đánh dấu `badChars = 1`. Điều này chứng tỏ flag hợp lệ chỉ sinh ra `local_9` nằm trong khoảng `[0, 36]`.

#### 2. Phép biến đổi toán học "Xoay Vòng" (Phần hack não nhất)

```c
if (local_9 != '$') {
  iVar3 = (local_9 + 0x12) % 0x24;
  bVar1 = (byte)(iVar3 >> 0x1f);
  local_9 = ((byte)iVar3 ^ bVar1) - bVar1;
}
```

* `0x12` là 18, `0x24` là 36.
* Đoạn code `((byte)iVar3 ^ bVar1) - bVar1` thực chất trong toán học chính là phép lấy **Giá trị tuyệt đối `abs()**` sau khi dịch và chia lấy dư.
* Công thức tổng quát: `local_9 = abs((local_9 + 18) % 36)`.
* **Hệ quả cực kỳ nguy hiểm:** Phép toán này là **phép toán nhiều-đối-một (Many-to-One)**. Ví dụ: Nếu `local_9` ban đầu là `0`, sau phép toán nó thành `18`. Nếu `local_9` ban đầu là `18`, sau phép toán nó cũng thành `0`.
* Điều này đồng nghĩa với việc: **Hai ký tự gốc khác nhau có thể bị biến đổi thành cùng một giá trị chỉ số `local_9` giống nhau, dẫn đến việc chúng dùng chung một chuỗi bit mã hóa!** Đây là lý do tại sao bài này khó hơn bài 1, chúng ta sẽ phải đối mặt với hiện tượng "đụng độ" (collision) ký tự khi giải mã.

#### 3. Cách tra cứu bảng Bit mới

```c
iVar3 = *(int *)(indexTable + (long)(local_9 + 1) * 4);
for (local_10 = *(int *)(indexTable + (long)(int)local_9 * 4); local_10 < iVar3; local_10 = local_10 + 1) {
  uVar2 = getValue(local_10);
  save(uVar2);
}
```

* Ở bài 1, bảng lưu độ dài và vị trí được gọi là `matrix`. Ở bài 2, nó đã đổi tên thành **`indexTable`**.
* Cách tra cứu cũng đổi: Thay vì mỗi ký tự chiếm 8 byte (gồm length và start_index), thì ở bài 2, `indexTable` là một mảng chứa các số `int` liên tiếp (mỗi số 4 byte).
* Vị trí bắt đầu của ký tự `local_9` là: `indexTable[local_9]`
* Vị trí kết thúc (không bao gồm) là: `indexTable[local_9 + 1]`
* Độ dài số bit cần lấy chính là: `indexTable[local_9 + 1] - indexTable[local_9]`

- Ta mở hàm getValue() và xem mảng secret thì ta thấy cơ chế cũng giống như bài 1 và mở mảng **indexTable[]** , ta thấy:
```
                             indexTable[144]                                 XREF[4,2]:   encode:00100dea(*), 
                             indexTable[148]                                              encode:00100df1(*), 
                             indexTable                                                   encode:00100e08(*), 
                                                                                          encode:00100e0f(*), 
                                                                                          encode:00100df1(R), 
                                                                                          encode:00100e0f(R)  
        00101360 00 00 00        undefine
                 00 04 00 
                 00 00 12 
           00101360 00              undefined100h                     [0]                               XREF[4]:     encode:00100dea(*), 
                                                                                                                     encode:00100df1(*), 
                                                                                                                     encode:00100e08(*), 
                                                                                                                     encode:00100e0f(*)  
```
- Dữ liệu từ Ghidra đã cho thấy rõ ràng sự thay đổi cấu trúc của `indexTable` so với bài 1.
- Nhìn vào cửa sổ **Listing** tại địa chỉ `00101360` của mảng `indexTable`, cấu trúc lưu trữ đã thay đổi:

* Thay vì lưu cặp số `(độ dài, vị trí)` như bài 1, bài 2 lưu theo dạng **mảng tích lũy vị trí bit** chứa các số nguyên `int` liên tiếp (mỗi số 4 byte).
* Dữ liệu thô tại đầu mảng `indexTable` là: `00 00 00 00` (giá trị 0), `04 00 00 00` (giá trị 4), `12 00 00 00` (giá trị 18)...
* Điều này khớp hoàn toàn với logic vòng lặp trong hàm `encode()`:
* Vị trí bit bắt đầu của index `local_9`: `start = indexTable[local_9]`
* Vị trí bit kết thúc của index `local_9`: `end = indexTable[local_9 + 1]`
* Chuỗi bit thực tế của ký tự này sẽ được cắt trong mảng `secret` từ đoạn `[start : end]`.
* Điểm mấu chốt nằm ở hàm toán băm ký tự
```c
iVar3 = (local_9 + 18) % 36;
local_9 = abs(iVar3); // Logic rút gọn từ phép toán bit dịch và XOR của Ghidra
```
Hàm `abs((local_9 + 18) % 36)` là một hàm **Many-to-One** (nhiều ký tự cho ra cùng một kết quả).

* Nếu `local_9` ban đầu là `0` $\rightarrow$ Kết quả là `18`.
* Nếu `local_9` ban đầu là `18` $\rightarrow$ Kết quả cũng là `18`.

**Hệ quả:** Có hai ký tự gốc khác nhau sẽ sở hữu **chung một chuỗi bit mã hóa**. Khi ta dịch ngược từ file `output`, tại vị trí chuỗi bit đó, ta sẽ thu được **2 ký tự khả dĩ**.

- Để giải quyết bẫy này, script giải mã của chúng ta không thể map cứng `1 chuỗi bit -> 1 ký tự` được nữa. Ta phải:

1. Dựng từ điển chứa **danh sách** các ký tự có thể có cho mỗi chuỗi bit: `{ chuỗi_bit : [ký_tự_1, ký_tự_2] }`.
2. Khi giải mã file `output`, ta sẽ thu được một danh sách các "lựa chọn" cho từng vị trí.
3. Sử dụng thuật toán tìm kiếm quay lui (Backtracking/DFS) để sinh ra tất cả các chuỗi flag có thể có, sau đó lọc ra chuỗi có nghĩa tiếng Anh.

- Ta viết script python solve.py => chạy chương trình => FLAG


# Note
