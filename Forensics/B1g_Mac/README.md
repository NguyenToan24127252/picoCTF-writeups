# Bài toán
- Description
    - Here's a zip file.

# Giải
- Bài toán cung cấp một file nén dạng `.zip`. Sau khi giải nén, chúng ta thu được một thư mục chứa các file ảnh `.bmp` (thư mục `test`) và một file thực thi Windows `main.exe`.

- Tên bài toán **"B1g_Mac"** gợi ý trực tiếp đến thuật ngữ **MAC times** (Modification, Access, Creation) — hệ thống mốc thời gian lưu trữ của tập tin trên phân vùng NTFS của Windows.

- Khi thực hiện phân tích tĩnh (Static Analysis) file thực thi `main.exe` bằng Ghidra, chúng ta phát hiện chương trình sử dụng các hàm Windows API (`GetFileTime`, `SetFileTime`) để can thiệp vào cấu trúc `FILETIME` 64-bit của các file ảnh trong thư mục `test`. Thay vì giấu tin trong dữ liệu ảnh (Steganography), tác giả đã ẩn giấu các byte của Flag trực tiếp vào **phần nano giây (các byte thấp `dwLowDateTime`)** của mốc thời gian tập tin nhằm tránh sự phát hiện của các lệnh liệt kê thông thường trên Linux.

- Ta sẽ analyze các hàm trong file main.exe

### Hàm `main`

```c
int __cdecl _main(int _Argc,char **_Argv,char **_Env)
{
  // ... (Khai báo biến)
  __main();
  _isOver = 0;
  local_28 = 0x65742f2e; // Hex của chuỗi "./te"
  local_24 = 0x7473;     // Hex của chuỗi "st"
  local_20 = 0;
  _folderName = &local_28; // Ghép lại thành đường dẫn "./test"
  local_14 = 0;            // Biến điều khiển chế độ (0 = Giấu tin, 1 = Giải mã)
  _pLevel = 0;
  
  local_18 = (FILE *)fopen("flag.txt","r");
  if (local_18 == (FILE *)0x0) {
    puts("No flag found, please make sure this is run on the server");
  }
  local_1c = fread(local_5a,1,0x12,local_18); // Đọc flag dài 0x12 (18 bytes)
  if (local_1c < 1) { exit(0); }
  
  _flag = local_5a;
  _flag_size = 0x12;
  local_60 = 0;
  _flag_index = &local_60;
  
  puts("Work is done!");
  listdir(local_14,_folderName); // Gọi hàm duyệt thư mục với param_1 = 0
  puts("Wait for 5 seconds to exit.");
  sleep(5);
  return 2;
}
```

* **Nhận xét:** Trong điều kiện bình thường chạy trên Server, hàm `main` mặc định gán `local_14 = 0`, nghĩa là file thực thi này chỉ chạy ở chế độ **Giấu tin** chứ không có tham số dòng lệnh nào giúp kích hoạt chế độ Giải mã.

### Hàm `listdir`

```c
void __cdecl listdir(int param_1,undefined4 param_2)
{
  // ...
  local_18 = FindFirstFileA(local_958,&local_158);
  if (local_18 != (HANDLE)0xffffffff) {
    local_10 = 1;
    local_11 = true;
    while (local_11 != false) {
      if ((strcmp(local_158.cFileName,".") != 0) && (strcmp(local_158.cFileName,"..") != 0)) {
        sprintf(local_958,"%s\\%s");
        if ((local_158.dwFileAttributes & 0x10) == 0) { // Nếu là tập tin
          if (local_10 == 1) {
            if (param_1 == 0) { hideInFile(local_958); }
            else if (param_1 == 1) { decodeBytes(local_958); }
          }
          local_10 = 1 - local_10; // Đảo trạng thái xen kẽ 1 -> 0 -> 1
        }
      }
      // ...
      BVar2 = FindNextFileA(local_18,&local_158);
      local_11 = BVar2 != 0;
    }
  }
}
```

* **Nhận xét:** Biến `local_10 = 1 - local_10` tạo ra cơ chế **đổi trạng thái cách quãng**. Điều này giải thích tại sao trong thư mục giải nén lại xuất hiện xen kẽ các cặp file gốc (bị giấu tin) và file `- Copy.bmp` (bị bỏ qua, giữ nguyên mốc thời gian gốc).

### Hàm `hideInFile` & `decodeBytes`

* Tại `hideInFile`, với cấu hình mặc định `_pLevel = 0`, chương trình lấy ra **2 byte** liên tiếp từ chuỗi Flag và gọi hàm `encodeBytes` ghi đè vào trường `dwLowDateTime` của mốc thời gian `local_2c` (tương ứng với **Modification Time - Mtime**).
```

/* hideInFile */

void __cdecl hideInFile(LPCSTR param_1)

{
  BOOL BVar1;
  _FILETIME local_2c;
  _FILETIME local_24;
  _FILETIME local_1c;
  char local_12;
  char local_11;
  HANDLE local_10;
  
  local_10 = CreateFileA(param_1,0x100,0,(LPSECURITY_ATTRIBUTES)0x0,3,0,(HANDLE)0x0);
  _DoNotUpdateLastAccessTime(local_10);
  if (local_10 == (HANDLE)0xffffffff) {
    printf("Error:INVALID_HANDLED_VALUE");
  }
  else {
    BVar1 = GetFileTime(local_10,&local_1c,&local_24,&local_2c);
    if (BVar1 == 0) {
      printf("Error: C-GFT-01");
    }
    else {
      local_11 = *(char *)(*_flag_index + _flag);
      *_flag_index = *_flag_index + 1;
      local_12 = *(char *)(*_flag_index + _flag);
      *_flag_index = *_flag_index + 1;
      encodeBytes(local_11,local_12,&local_2c.dwLowDateTime);
      if (0 < _pLevel) {
        local_11 = *(char *)(*_flag_index + _flag);
        *_flag_index = *_flag_index + 1;
        local_12 = *(char *)(*_flag_index + _flag);
        *_flag_index = *_flag_index + 1;
        encodeBytes(local_11,local_12,&local_1c.dwLowDateTime);
      }
      if (_pLevel == 2) {
        local_11 = *(char *)(*_flag_index + _flag);
        *_flag_index = *_flag_index + 1;
        local_12 = *(char *)(*_flag_index + _flag);
        *_flag_index = *_flag_index + 1;
        encodeBytes(local_11,local_12,&local_24.dwLowDateTime);
      }
      BVar1 = SetFileTime(local_10,&local_1c,&local_24,&local_2c);
      if (BVar1 == 0) {
        printf("Error: C-SFT-01");
      }
      else {
        if (_flag_size <= *_flag_index) {
          _isOver = 1;
        }
        CloseHandle(local_10);
      }
    }
  }
  return;
}
```
* Ngược lại, hàm `decodeBytes` thực hiện bốc chính xác 2 byte thấp nhất từ trường `dwLowDateTime` của mốc thời gian sửa đổi tập tin nhằm tái tạo lại chuỗi Flag nguyên bản.
```
/* decodeBytes */

void __cdecl decodeBytes(LPCSTR param_1)

{
  BOOL BVar1;
  undefined4 local_40;
  undefined1 local_3c;
  undefined3 uStack_3b;
  undefined4 local_38;
  _FILETIME local_34;
  _FILETIME local_2c;
  _FILETIME local_24;
  int local_1c;
  uint local_18;
  HANDLE local_14;
  int local_10;
  
  local_14 = CreateFileA(param_1,0x80,0,(LPSECURITY_ATTRIBUTES)0x0,3,0,(HANDLE)0x0);
  _DoNotUpdateLastAccessTime(local_14);
  if (local_14 == (HANDLE)0xffffffff) {
    printf("error loading the file");
  }
  else {
    BVar1 = GetFileTime(local_14,&local_24,&local_2c,&local_34);
    if (BVar1 == 0) {
      printf("error getting the times of the file");
    }
    else {
      local_38 = 0;
      local_40 = CONCAT13((char)(local_24.dwLowDateTime & 0xffff),
                          CONCAT12((char)((local_24.dwLowDateTime & 0xffff) >> 8),
                                   (short)CONCAT31((int3)local_34.dwLowDateTime,
                                                   (char)(local_34.dwLowDateTime >> 8))));
      local_18 = local_2c.dwLowDateTime & 0xffff;
      _local_3c = CONCAT31(CONCAT21(0x6472,(char)local_18),(char)(local_18 >> 8));
      local_1c = (_pLevel + 1) * 2;
      local_10 = 0;
      while ((local_10 < local_1c && (*_buff_index < _buff_size))) {
        *(undefined1 *)(_buff + *_buff_index) = *(undefined1 *)((int)&local_40 + local_10);
        *_buff_index = *_buff_index + 1;
        local_10 = local_10 + 1;
      }
      if (_buff_size <= *_buff_index) {
        _isOver = 1;
      }
    }
  }
  return;
}
```
## Giải pháp 
- Qua phân tích mã nguồn bằng Ghidra, chúng ta nhận thấy hàm `decodeBytes` chỉ thực hiện bóc tách dữ liệu từ mốc thời gian thô rồi ghi vào một vùng đệm bộ nhớ trống (`_buff`) chứ bản thân nó hoàn toàn không có lệnh in kết quả (`printf` hay `puts`).

- Đoạn mã chịu trách nhiệm gọi tiến trình giải mã xen kẽ và thực hiện in Flag ra màn hình Console thực chất nằm ở một hàm ẩn, hoàn toàn không được gọi từ `main`, mang tên **`_decode`** (địa chỉ bộ nhớ tại `00401afe`):

```c
void _decode(void)
{
  // ... (Khởi tạo con trỏ vùng đệm)
  _buff_size = 0x12;
  _buff = &local_24;
  _buff_index = &local_28;
  
  _listdir(1, _folderName);               // Gọi listdir ở chế độ giải mã (param_1 = 1)
  printf("value of DECODE %s \n", _buff); // Lệnh xuất Flag nằm tại đây
  puts("Wait for 5 seconds to exit.");
  _sleep(5);
  exit(0);
}
```

- Tuy nhiên, do các cơ chế bảo vệ vùng nhớ Stack của các hệ điều hành Windows hiện đại (hoặc lớp tương thích Wine trên Linux) rất nghiêm ngặt, việc sử dụng các kỹ thuật can thiệp vào thanh ghi để bẻ lái luồng thực thi (`EIP Hijacking`) nhảy ngang hông vào hàm `_decode` rất dễ dẫn đến hiện tượng crash ngầm (tiến trình bị hủy bởi `NtTerminateProcess` trước khi kịp in kết quả).

- Do đó, phương pháp Forensics tối ưu, ổn định và tự động hóa cao nhất là viết một **Script Python chạy trực tiếp trên Windows** để tương tác với hệ thống file.

### Bước 1: Khôi phục hiện trạng dữ liệu gốc

- Vì mốc thời gian nano giây của tệp tin có thể đã bị thay đổi hoặc ghi đè trong các lần chạy thử nghiệm trước đó, việc làm sạch và giải nén lại phân vùng là bắt buộc:

1. Xóa thư mục lỗi cũ: `rmdir /s /q test`
2. Sử dụng phần mềm **7-Zip** hoặc **WinRAR** giải nén lại tệp tin `b1g_mac.zip`.

> *Lưu ý:* Tuyệt đối không sử dụng trình giải nén mặc định của Linux (`unzip`) hoặc tính năng "Extract All" mặc định của Windows vì các công cụ này thường làm tròn mốc thời gian về dạng giây (`.0000000`), làm mất hoàn toàn cấu trúc dữ liệu của Flag.

### Bước 2: Xây dựng Script trích xuất tự động (`solve.py`)

- Tạo một file tên là `solve.py` nằm ngay cạnh thư mục `test` và file `main.exe` với nội dung sử dụng thư viện `ctypes` để gọi trực tiếp Windows API => chạy script => FLAG

# Note 

* **Kỹ thuật Giấu tin Anti-Forensics (Timestomp):** Bài toán minh họa một phương thức ẩn giấu dữ liệu vô hình đối với các bộ lọc thông thường. Windows hiển thị thời gian ở giao diện ngoài chỉ tới đơn vị Giờ:Phút:Giây, nhưng cấu trúc `FILETIME` trên phân vùng **NTFS** có độ phân giải thực tế lên đến **100 nanosecond**. Tác giả đã tận dụng các bit dư thừa ở hàng đơn vị nano giây siêu nhỏ này để nhét các ký tự ASCII của Flag vào.
* **Bẫy môi trường và Hệ thống tệp tin (NTFS vs ext4):** Hệ thống file của Linux (như ext4) quản lý mốc thời gian theo chuẩn Unix Epoch (tính từ năm 1970), khác hoàn toàn với NTFS của Windows (tính từ năm 1601). Quá trình giải nén thông thường trên Linux sẽ thực hiện phép toán chuyển đổi mốc thời gian, vô tình làm sai lệch hoặc cắt cụt (làm tròn) các byte ở đuôi nano giây, trực tiếp phá hủy Flag. Do đó các bài toán dạng MAC times bắt buộc phải được xử lý trên môi trường Windows gốc hoặc các công cụ bảo toàn thuộc tính như `7z`.
* **Thứ tự duyệt file (Directory Indexing):** Hàm `FindFirstFileA` / `FindNextFileA` của Windows quét thư mục dựa trên cấu trúc bảng chỉ mục B-tree của NTFS, dẫn đến việc các file có đuôi ` - Copy.bmp` được đẩy lên đọc trước. Sự khác biệt này khiến việc sử dụng các hàm liệt kê thư mục mặc định của Linux (`os.listdir`) trả về sai trình tự, làm các ký tự của chuỗi Flag bị đảo lộn cấu trúc.