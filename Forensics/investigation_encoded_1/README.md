# Bài toán
- Description
    - What can you make of this?
We have recovered a binary and 1 file: image01. See what you can make of it. NOTE: The flag is not in the normal picoCTF{XXX} format.

# Giải
## GIAI ĐOẠN 1
- Ta check xem 2 file đó là gì
```
┌──(kali㉿kali)-[/mnt/hgfs/picoCTF-writeups/Forensics/investigation_encoded_1]
└─$ file output                                      
output: Non-ISO extended-ASCII text, with no line terminators
                                                                                                                                                                                                                  
┌──(kali㉿kali)-[/mnt/hgfs/picoCTF-writeups/Forensics/investigation_encoded_1]
└─$ file mystery
mystery: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=db5601ad9bc8fe49e075defba61295a1ecfc4db1, for GNU/Linux 3.2.0, not stripped
```
- Thì ta thấy mystery là 1 file thực thi có thể nó chính là thủ phạm mã hóa dữ liệu; file output là file chứa dữ liệu bị mã hóa dưới dạng ASCII mở rộng => có thể nó sẽ là nơi tìm ra flag
- Sử dụng ghidra để analyze file mystery

## GIAI ĐOẠN 2
- Analyze hàm main:
```
undefined8 main(void)

{
  long lVar1;
  size_t sVar2;
  long in_FS_OFFSET;
  undefined4 local_20;
  int local_1c;
  FILE *local_18;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_18 = fopen("flag.txt","r");
  if (local_18 == (FILE *)0x0) {
    fwrite("./flag.txt not found\n",1,0x15,stderr);
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  flag_size = 0;
  fseek(local_18,0,2);
  lVar1 = ftell(local_18);
  flag_size = (int)lVar1;
  fseek(local_18,0,0);
  if (0xfffe < flag_size) {
    fwrite("Error, file bigger that 65535\n",1,0x1e,stderr);
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  flag = malloc((long)flag_size);
  sVar2 = fread(flag,1,(long)flag_size,local_18);
  local_1c = (int)sVar2;
  if (local_1c < 1) {
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  local_20 = 0;
  flag_index = &local_20;
  output = fopen("output","w");
  buffChar = 0;
  remain = 7;
  fclose(local_18);
  encode();
  fclose(output);
  fwrite("I\'m Done, check ./output\n",1,0x19,stderr);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```
- Nhìn chung, hàm `main` này đóng vai trò chuẩn bị dữ liệu chứ chưa trực tiếp thực hiện thuật toán mã hóa (thuật toán nằm ở hàm `encode()`):
1. **Mở file flag:** Nó tìm và mở file `flag.txt` để đọc (`fopen("flag.txt","r")`).
2. **Kiểm tra kích thước:** Nó đo dung lượng file `flag.txt`. Nếu file lớn hơn 65535 bytes (`0xfffe`), nó sẽ báo lỗi và dừng chương trình.
3. **Đọc dữ liệu vào bộ nhớ:** Nó cấp phát bộ nhớ (`malloc`) dựa trên kích thước của flag, sau đó đọc toàn bộ nội dung file flag vào một biến toàn cục tên là `flag`.
4. **Khởi tạo các biến mã hóa:**
* Mở file `output` để chuẩn bị ghi kết quả (`fopen("output","w")`).
* Đặt một biến chỉ số (index) để duyệt flag: `flag_index = &local_20;` (với `local_20 = 0`, tức là bắt đầu từ ký tự đầu tiên).
* Khởi tạo hai biến rất đáng nghi: `buffChar = 0;` và `remain = 7;`. Hai biến này thường xuất hiện trong các thuật toán **mã hóa dạng Bit-stream (ghi dữ liệu theo từng bit thay vì từng byte)**.
5. **Mã hóa:** Gọi hàm `encode();` để xử lý.
6. **Kết thúc:** Đóng file `output` và in ra câu thông báo `"I'm Done, check ./output"`.

- Tiếp theo ta sẽ analyze hàm encode()
```
void encode(void)

{
  char cVar1;
  char cVar2;
  int iVar3;
  undefined4 uVar4;
  char local_15;
  int local_14;
  
  while( true ) {
    if (flag_size <= *flag_index) {
      while (remain != 7) {
        save(0);
      }
      return;
    }
    cVar1 = *(char *)(*flag_index + flag);
    cVar2 = isValid((int)cVar1);
    if (cVar2 != '\x01') break;
    local_15 = lower((int)cVar1);
    if (local_15 == ' ') {
      local_15 = '{';
    }
    local_14 = *(int *)(matrix + (long)(local_15 + -0x61) * 8 + 4);
    iVar3 = local_14 + *(int *)(matrix + (long)(local_15 + -0x61) * 8);
    for (; local_14 < iVar3; local_14 = local_14 + 1) {
      uVar4 = getValue(local_14);
      save(uVar4);
    }
    *flag_index = *flag_index + 1;
  }
  fwrite("Error, I don\'t know why I crashed\n",1,0x22,stderr);
                    /* WARNING: Subroutine does not return */
  exit(1);
}
```
- Hàm `encode()` này là một thuật toán **mã hóa nén bit (Bit-stream encoding)**, rất giống với nguyên lý của **Mã hóa Huffman** (Huffman Coding). Thay vì ghi 1 ký tự thành 1 byte (8 bit) ra file, nó sẽ biến đổi ký tự đó thành một chuỗi các bit có độ dài ngắn/dài khác nhau và nhồi các bit đó vào file `output`.

### Phân tích chi tiết hàm `encode()`

1. **Vòng lặp chính (`while(true)`):**
Nó sẽ duyệt qua từng ký tự của chuỗi `flag` cho đến khi `*flag_index` đạt đến `flag_size` (hết file).
* Nếu hết file, nó kiểm tra xem biến `remain` (số bit còn trống trong buffer byte hiện tại) có bằng 7 không. Nếu khác 7 (tức là còn bit lẻ chưa ghi), nó sẽ gọi `save(0)` để chèn thêm các bit `0` cho đủ 1 byte rồi mới thoát.

2. **Kiểm tra ký tự hợp lệ (`isValid`):**
* Nó lấy ký tự hiện tại: `cVar1 = *(char *)(*flag_index + flag);`
* Nó kiểm tra bằng hàm `isValid`. Nếu ký tự không hợp lệ, chương trình sẽ crash ngay lập tức. Điều này chứng tỏ toàn bộ các ký tự trong flag đều là ký tự hợp lệ đối với chương trình.

3. **Chuẩn hóa ký tự (`lower`):**
* Nó chuyển ký tự thành chữ thường thông qua hàm `lower`.
* **Đặc biệt:** Nếu ký tự là khoảng trắng `' '`, nó sẽ biến thành ký tự `'{'` (dấu ngoặc nhọn mở)!!!!

4. **Tra cứu bảng Mã hóa (`matrix`):**
Đoạn này là phần cốt lõi của thuật toán:
```c
local_14 = *(int *)(matrix + (long)(local_15 + -0x61) * 8 + 4);
iVar3 = local_14 + *(int *)(matrix + (long)(local_15 + -0x61) * 8);
```

* `0x61` chính là ký tự `'a'` trong bảng mã ASCII. Đoạn `local_15 + -0x61` nghĩa là lấy `ký_tự - 'a'` để tìm ra chỉ số (index) của ký tự đó trong một mảng tên là `matrix`.
* Mảng `matrix` này chứa thông tin về vị trí bắt đầu và độ dài (số lượng bit) của từng ký tự.
* Vòng lặp `for` ngay sau đó sẽ chạy từ vị trí `local_14` đến `iVar3`, lấy từng bit bằng hàm `getValue(local_14)` rồi nhét vào hàm `save(uVar4)` để ghi ra file `output`.

- Tiếp theo ta sẽ analyze hàm save() để xem nó nối bit từ trái sang phải hay ngược lại ; hàm getValue() xem nó lấy dữ liệu từ mảng nào;  mảng matrix để xem giá trị lưu trữ tại vùng nhớ đó là gì.

```
uint getValue(int param_1)

{
  int iVar1;
  
  iVar1 = param_1;
  if (param_1 < 0) {
    iVar1 = param_1 + 7;
  }
  return (int)(uint)(byte)secret[iVar1 >> 3] >> (7U - (char)(param_1 % 8) & 0x1f) & 1;
}
```
---
```
void save(byte param_1)

{
  buffChar = buffChar | param_1;
  if (remain == 0) {
    remain = 7;
    fputc((int)(char)buffChar,output);
    buffChar = '\0';
  }
  else {
    buffChar = buffChar * '\x02';
    remain = remain + -1;
  }
  return;
}
```
``` 
mảng matrix
                             matrix[4]                                       XREF[2,4]:   encode:00101468(*), 
                             matrix[208]                                                  encode:0010146f(*), 
                             matrix[212]                                                  encode:0010144a(*), 
                             matrix                                                       encode:00101451(*), 
                                                                                          encode:00101451(R), 
                                                                                          encode:0010146f(R)  
        00102060 08 00 00        undefine
                 00 00 00 
                 00 00 0c 
           00102060 08              undefined108h                     [0]                               XREF[2]:     encode:00101468(*), 
                                                                                                                     encode:0010146f(*)  
```
### 1. Phân tích hàm `save(byte param_1)` - Cách các bit được ghi

Hàm này chịu trách nhiệm gom các bit (`0` hoặc `1`) thành một byte hoàn chỉnh trước khi ghi vào file `output`:

* `buffChar = buffChar | param_1;` -> Gộp bit mới vào vị trí thấp nhất (Lập luận từ dòng nhân 2 phía dưới).
* Nếu chưa đủ 8 bit (`remain != 0`), nó thực hiện: `buffChar = buffChar * \x02; remain = remain - 1;`
* Phép nhân 2 (`* 2`) trong hệ nhị phân tương đương với **dịch trái 1 bit (`<< 1`)**.


* **Kết luận:** Dữ liệu được đẩy vào từ **phải qua trái (MSB-first)**. Khi ta đọc file `output`, ta chỉ cần chuyển từng byte thành chuỗi bit 8 ký tự (ví dụ: `01101000`). Toàn bộ file `output` sẽ biến thành một chuỗi bit dài liên tục.

---

### 2. Phân tích hàm `getValue(int param_1)` - Nguồn gốc các bit

Hàm này lấy bit từ một mảng tên là `secret`:

```c
return (int)(uint)(byte)secret[iVar1 >> 3] >> (7U - (char)(param_1 % 8) & 0x1f) & 1;
```

* `iVar1 >> 3` tương đương với `param_1 / 8` để tìm vị trí byte trong mảng `secret`.
* `7U - (param_1 % 8)` chứng tỏ mảng `secret` cũng được đọc bit theo thứ tự từ trái qua phải.
* **Kết luận:** Có một mảng dữ liệu bit khổng lồ tên là `secret`. Biến `local_14` (được tra từ `matrix`) chính là **vị trí bit bắt đầu** (bit index), và vòng lặp trong `encode` sẽ lấy ra liên tiếp một số lượng bit nhất định từ mảng `secret` này để đại diện cho ký tự.

---

### 3. Phân tích cấu trúc mảng `matrix`

Nhìn vào cửa sổ **Listing** ở giữa hình ảnh của bạn, ta thấy cấu trúc của mảng `matrix`:

* Mỗi phần tử trong `matrix` chiếm **8 byte** (gồm hai số nguyên `int`, mỗi số 4 byte).
* `int` thứ nhất (4 byte đầu): Độ dài chuỗi bit (số lượng bit cần lấy).
* `int` thứ hai (4 byte sau): Vị trí bắt đầu (`start_index`) trong mảng `secret`.


* Trong hình, tại địa chỉ `00102060`:
* Hàng `[0]` (đại diện cho ký tự `'a'`): `08 00 00 00` (độ dài = 8) và `00 00 00 00` (vị trí = 0).
* Hàng `[4]` (đại diện cho ký tự `'e'`): `08 00 00 00` (độ dài = 8) và `0c 00 00 00` (vị trí = 12 hay `0x0c`).

- Bây giờ ta có thể mườn tượng được luồng hoạt động của nó:
```
[ File flag.txt ] 
       │
       ▼
( Hàm main ) ──► Đọc toàn bộ ký tự vào bộ nhớ RAM
       │
       ▼
( Hàm encode ) ──► Duyệt từng ký tự ──► Chuyển thành chữ thường (lower)
                                                │
                                                ▼
                                    Tra cứu bảng [ matrix ]
                                    để lấy (Vị trí, Độ dài bit)
                                                │
                                                ▼
                                    Bốc tách các bit tương ứng 
                                    từ mảng tĩnh [ secret ]
                                                │
                                                ▼
( Hàm save ) ◄──────────────────────────────────┘
       │
       ├─► Nhồi bit vào biến đệm buffChar (từ phải qua trái)
       │
       └─► Khi đủ 8 bit ──► Ghi 1 byte thô ra [ File output ]

```
- Tiếp theo ta sẽ analyze mảng tĩnh secret
```
                             secret                                          XREF[2]:     getValue:0010130a(*), 
                                                                                          getValue:00101311(*)  
        00102020 b8 ea 8e        undefine
                 ba 3a 88 
                 ae 8e e8 
           00102020 b8              undefined1B8h                     [0]                               XREF[2]:     getValue:0010130a(*), 
                                                                                                                     getValue:00101311(*)  
```
- **Kết luận** : địa chỉ mảng secret như ta thấy bắt đầu tại 00102020 -> bây giờ viết script tự động đọc trực tiếp mảng secret và matrix sau đó dịch ngược file output 
- Chạy solve.py =>FLAG

# Note

### 1. Bản chất thuật toán và Vai trò của mảng `secret`

* **Cơ chế mã hóa:** Bài toán này sử dụng một dạng custom của **Mã hóa Huffman (Huffman Coding / Bit-stream encoding)**. Thay vì lưu một ký tự cố định bằng 1 byte (8 bit) như thông thường, thuật toán biến đổi mỗi chữ cái thành một chuỗi bit có độ dài biến thiên (ví dụ: chữ `'a'` có thể chỉ cần 3 bit, chữ `'b'` cần 5 bit).
* **Tại sao cần mảng `secret`?** Trong ngôn ngữ C, việc quản lý và ghi các chuỗi bit có độ dài lửng lơ (không tròn byte) ra file rất phức tạp nếu lưu riêng rẽ. Vì vậy, tác giả đã nối toàn bộ các chuỗi bit đại diện của bảng chữ cái thành một **dải bit duy nhất, dài liên tục**, rồi nén dải bit đó vào các byte của mảng tĩnh `secret`.
* **Mối quan hệ giữa `matrix` và `secret`:** Mảng `matrix` đóng vai trò như một quyển "mục lục", lưu trữ `vị trí bắt đầu (start_index)` và `độ dài (length)` của từng ký tự trên dải bit `secret`. Khi mã hóa một chữ cái, chương trình chỉ cần tra cứu mục lục `matrix`, nhảy đến đúng vị trí trên cuộn băng `secret`, cắt ra số lượng bit cần thiết rồi gửi qua hàm `save()`.

### 2. Logic xử lý Bit trong hàm `save()` và `getValue()`

* **Hàm `getValue()` (Đọc bit):** Đoạn code `7U - (param_1 % 8)` cho thấy chương trình trích xuất bit từ trái qua phải (từ bit có trọng số cao nhất MSB đến bit thấp nhất LSB) trong từng byte của mảng `secret`.
* **Hàm `save()` (Ghi bit):** Phép toán `buffChar = buffChar * '\x02'` (tương đương với dịch trái 1 bit `<< 1`) kết hợp với phép `OR | param_1` chứng tỏ các bit mã hóa được nhồi vào biến đệm từ phải qua trái. Khi gom đủ 8 bit (`remain == 0`), byte đó mới được ghi ra file `output`. Đây là cơ chế **MSB-First**. Do đó, khi giải mã file `output`, ta cũng phải rã từng byte thành chuỗi 8 bit theo đúng thứ tự từ trái qua phải.

### 3. Tại sao Script giải mã lại quét toàn bộ 256 ký tự ASCII?

* Mặc dù trong hàm `encode()` của Ghidra chỉ hiển thị đoạn code xử lý chữ thường từ `'a'` đến `'{'` (`local_15 + -0x61`), nhưng trên thực tế, một file thực thi có thể chứa các đoạn logic kiểm tra ẩn hoặc các phần tử mở rộng trong bảng `matrix` dành cho ký tự đặc biệt (như số, dấu gạch dưới, ngoặc nhọn).
* Việc viết script Python quét toàn bộ phạm vi từ `0` đến `255` (Brute-force cấu trúc `matrix`) giúp ta tự động "bắt" được toàn bộ các chuỗi bit đại diện cho mọi ký tự có khả năng xuất hiện mà không sợ bị lọt lưới.

