# Bài toán
- Description
    - We have recovered a binary and a few images: image, image2, image3. See what you can make of it. There should be a flag somewhere.

# Giải
- Tương tự như bài 1 ta tiến hành analyze trên file execute mystery trên ghidra
- hàm main:
```

void main(void)

{
  FILE *__stream;
  FILE *__stream_00;
  FILE *__stream_01;
  FILE *__stream_02;
  long in_FS_OFFSET;
  char local_6b;
  int local_68;
  int local_64;
  int local_60;
  char local_38 [4];
  char local_34;
  char local_33;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  __stream = fopen("flag.txt","r");
  __stream_00 = fopen("mystery.png","a");
  __stream_01 = fopen("mystery2.png","a");
  __stream_02 = fopen("mystery3.png","a");
  if (__stream == (FILE *)0x0) {
    puts("No flag found, please make sure this is run on the server");
  }
  if (__stream_00 == (FILE *)0x0) {
    puts("mystery.png is missing, please run this on the server");
  }
  fread(local_38,0x1a,1,__stream);
  fputc((int)local_38[1],__stream_02);
  fputc((int)(char)(local_38[0] + '\x15'),__stream_01);
  fputc((int)local_38[2],__stream_02);
  local_6b = local_38[3];
  fputc((int)local_33,__stream_02);
  fputc((int)local_34,__stream_00);
  for (local_68 = 6; local_68 < 10; local_68 = local_68 + 1) {
    local_6b = local_6b + '\x01';
    fputc((int)local_38[local_68],__stream_00);
  }
  fputc((int)local_6b,__stream_01);
  for (local_64 = 10; local_64 < 0xf; local_64 = local_64 + 1) {
    fputc((int)local_38[local_64],__stream_02);
  }
  for (local_60 = 0xf; local_60 < 0x1a; local_60 = local_60 + 1) {
    fputc((int)local_38[local_60],__stream_00);
  }
  fclose(__stream_00);
  fclose(__stream);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```
- Lần này chương trình đọc flag ra và phân tán (split) các ký tự vào cả **3 file**: `mystery.png`, `mystery2.png`, và `mystery3.png`.

- Tuy nhiên, cấu trúc bộ nhớ trên Stack vẫn tương tự: `fread` đọc **0x1a (26) bytes** liên tục vào mảng bắt đầu từ `local_38`. Như vậy, ta có thể ánh xạ các biến cục bộ thành các chỉ số của flag từ `0` đến `25` như sau:

* `local_38[0]` đến `local_38[3]` $\rightarrow$ `flag[0]` đến `flag[3]`
* `local_34` $\rightarrow$ `flag[4]`
* `local_33` $\rightarrow$ `flag[5]`
* `local_38[i]` $\rightarrow$ `flag[i]` (với các chỉ số lớn hơn)

## 1. Trace logic ghi file chi tiết từng bước

Ta đi theo thứ tự thực thi của mã nguồn từ trên xuống dưới:

1. `fputc((int)local_38[1], __stream_02);`
$\rightarrow$ Ghi `flag[1]` vào **mystery3.png** (giữ nguyên).
2. `fputc((int)(char)(local_38[0] + '\x15'), __stream_01);`
$\rightarrow$ Ghi `flag[0] + 0x15` vào **mystery2.png**.
3. `fputc((int)local_38[2], __stream_02);`
$\rightarrow$ Ghi `flag[2]` vào **mystery3.png** (giữ nguyên).
4. `local_6b = local_38[3];`
$\rightarrow$ Khởi tạo biến tạm `local_6b` bằng giá trị của `flag[3]`.
5. `fputc((int)local_33, __stream_02);`
$\rightarrow$ Ghi `flag[5]` vào **mystery3.png** (giữ nguyên).
6. `fputc((int)local_34, __stream_00);`
$\rightarrow$ Ghi `flag[4]` vào **mystery.png** (giữ nguyên).
7. **Vòng lặp từ 6 đến 9 (`local_68 = 6; local_68 < 10`):**
* Vòng lặp chạy 4 lần ứng với các chỉ số `6, 7, 8, 9`.
* Mỗi vòng lặp, `local_6b` tăng thêm 1: `local_6b = local_6b + 1`. Vì ban đầu `local_6b = flag[3]`, sau khi kết thúc vòng lặp này, `local_6b` sẽ có giá trị là `flag[3] + 4`.
* Ghi `flag[6], flag[7], flag[8], flag[9]` vào **mystery.png** (giữ nguyên).


8. `fputc((int)local_6b, __stream_01);`
$\rightarrow$ Ghi giá trị lúc này của `local_6b` (tức là `flag[3] + 4`) vào **mystery2.png**.
9. **Vòng lặp từ 10 đến 14 (`local_64 = 10; local_64 < 0xf`):**
$\rightarrow$ Ghi `flag[10]` đến `flag[14]` vào **mystery3.png** (giữ nguyên).
10. **Vòng lặp từ 15 đến 25 (`local_60 = 0xf; local_60 < 0x1a`):**
$\rightarrow$ Ghi `flag[15]` đến `flag[25]` vào **mystery.png** (giữ nguyên).

---

## 2. Tổng hợp vị trí phân tán của Flag

Để giải bài này, ta cần lấy các byte bị append (nằm ở cuối cùng) của cả 3 file PNG.

* Hãy gọi byte cuối cùng lấy từ `mystery.png` là mảng `m1`.
* Byte lấy từ `mystery2.png` là mảng `m2`.
* Byte lấy từ `mystery3.png` là mảng `m3`.

Dựa vào trace ở trên, số lượng byte được thêm vào cuối mỗi file là:

* **mystery.png** nhận được 1 + 4 + 11 = **16 bytes**.
* **mystery2.png** nhận được 1 + 1 = **2 bytes**.
* **mystery3.png** nhận được 1 + 1 + 1 + 5 = **8 bytes**.
*(Tổng cộng: 16 + 2 + 8 = 26 bytes ứng với độ dài ban đầu).*

Bản đồ khôi phục flag từ dữ liệu trích xuất của 3 file sẽ như sau:

| Chỉ số Flag | Nguồn lấy từ file | Công thức khôi phục |
| --- | --- | --- |
| `flag[0]` | `m2[0]` (Byte đầu tiên trích từ file 2) | `m2[0] - 0x15` |
| `flag[1]` | `m3[0]` (Byte thứ 1 trích từ file 3) | Giữ nguyên |
| `flag[2]` | `m3[1]` | Giữ nguyên |
| `flag[3]` | `m2[1]` (Byte thứ 2 trích từ file 2) | `m2[1] - 4` |
| `flag[4]` | `m1[0]` (Byte thứ 1 trích từ file 1) | Giữ nguyên |
| `flag[5]` | `m3[2]` | Giữ nguyên |
| `flag[6]` đến `flag[9]` | `m1[1]` đến `m1[4]` | Giữ nguyên |
| `flag[10]` đến `flag[14]` | `m3[3]` đến `m3[7]` | Giữ nguyên |
| `flag[15]` đến `flag[25]` | `m1[5]` đến `m1[15]` | Giữ nguyên |
