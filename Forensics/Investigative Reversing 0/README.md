# Bài toán
- Description
    - We have recovered a binary and an image. See what you can make of it. There should be a flag somewhere.

# Giải
- Bài này cho ta 2 file png mystery và 1 file thực thi mystery -> tiến hành analyze file mystery = ghidra
- hàm main:
```

void main(void)

{
  FILE *__stream;
  FILE *__stream_00;
  size_t sVar1;
  long in_FS_OFFSET;
  int local_54;
  int local_50;
  char local_38 [4];
  char local_34;
  char local_33;
  char local_29;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  __stream = fopen("flag.txt","r");
  __stream_00 = fopen("mystery.png","a");
  if (__stream == (FILE *)0x0) {
    puts("No flag found, please make sure this is run on the server");
  }
  if (__stream_00 == (FILE *)0x0) {
    puts("mystery.png is missing, please run this on the server");
  }
  sVar1 = fread(local_38,0x1a,1,__stream);
  if ((int)sVar1 < 1) {
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  puts("at insert");
  fputc((int)local_38[0],__stream_00);
  fputc((int)local_38[1],__stream_00);
  fputc((int)local_38[2],__stream_00);
  fputc((int)local_38[3],__stream_00);
  fputc((int)local_34,__stream_00);
  fputc((int)local_33,__stream_00);
  for (local_54 = 6; local_54 < 0xf; local_54 = local_54 + 1) {
    fputc((int)(char)(local_38[local_54] + '\x05'),__stream_00);
  }
  fputc((int)(char)(local_29 + -3),__stream_00);
  for (local_50 = 0x10; local_50 < 0x1a; local_50 = local_50 + 1) {
    fputc((int)local_38[local_50],__stream_00);
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
- Dựa vào đoạn code thu được từ Ghidra, ta có thể phân tích cách mà chương trình `mystery` đã giấu flag vào file `mystery.png`. Đây là một bài toán Steganography/Reverse Engineering cơ bản: flag được đọc từ `flag.txt` và được **append (ghi nối tiếp)** vào cuối file `mystery.png`.

## 1. Phân tích cấu trúc Stack & Biến cục bộ

Ghidra nhận diện các biến cục bộ một cách riêng lẻ, nhưng dựa vào hàm `fread(local_38, 0x1a, 1, __stream);`, ta thấy chương trình đọc **0x1a (26) bytes** từ file flag vào một mảng liên tục bắt đầu từ địa chỉ của `local_38`.

Do cách sắp xếp biến trên Stack (Stack Layout), các biến đứng sau thực chất là các phần tử tiếp theo của chuỗi flag:

* `local_38` (mảng 4 bytes): tương ứng với các chỉ số `flag[0]` đến `flag[3]`
* `local_34`: tương ứng với `flag[4]`
* `local_33`: tương ứng với `flag[5]`
* `local_38[local_54]` (trong vòng lặp từ 6 đến 14): tương ứng với `flag[6]` đến `flag[14]`
* `local_29`: tương ứng với `flag[15]`
* `local_38[local_50]` (trong vòng lặp từ 16 đến 25): tương ứng với `flag[16]` đến `flag[25]`

> **Tóm lại:** Flag có độ dài chuẩn là **26 ký tự** (từ chỉ số 0 đến 25).

---

## 2. Thuật toán mã hóa & Ghi file

Chương trình mở file `mystery.png` với chế độ `"a"` (append), nghĩa là dữ liệu flag bị biến đổi sẽ nằm ở **cuối cùng** của file PNG ban đầu.

Quá trình ghi dữ liệu diễn ra theo 5 giai đoạn:

| Giai đoạn | Chỉ số trong Flag (Ký tự gốc) | Thao tác ghi vào file |
| --- | --- | --- |
| **1** | `0` đến `3` | Giữ nguyên: `fputc(flag[0] -> flag[3])` |
| **2** | `4`, `5` | Giữ nguyên: `fputc(flag[4])`, `fputc(flag[5])` |
| **3** | `6` đến `14` (`0x0f - 1`) | **Cộng thêm 5**: `fputc(flag[i] + 5)` |
| **4** | `15` | **Trừ đi 3**: `fputc(flag[15] - 3)` |
| **5** | `16` (`0x10`) đến `25` (`0x1a - 1`) | Giữ nguyên: `fputc(flag[i])` |

---

## 3. Cách lấy dữ liệu bị giấu (Extract)

Vì flag được append vào cuối file `mystery.png`, ta cần lấy **26 bytes cuối cùng** của file `mystery.png` đã bị chỉnh sửa để tiến hành giải mã ngược lại.

Trong cấu trúc file PNG, một file chuẩn luôn kết thúc bằng 4 bytes của block IEND: `\x49\x45\x4e\x44\xae\x42\x60\x82` (hoặc ngắn gọn là kết thúc tại cụm `IEND`). Bất kỳ dữ liệu nào nằm *sau* cụm này chính là phần flag được thêm vào.

---

## 4. Thuật toán giải mã ngược (Reverse Script)

Để tìm lại flag gốc, ta đảo ngược các phép toán ở Giai đoạn 3 và Giai đoạn 4:

* Từ chỉ số `6` đến `14`: Lấy byte trong file **trừ đi 5**.
* Tại chỉ số `15`: Lấy byte trong file **cộng thêm 3**.
* Các chỉ số còn lại giữ nguyên.

- Chạy script => FLAG