# Bài toán
- Description
    - Here's a zip file.

# Giải
- Bài toán cung cấp một file nén dạng `.zip`. Sau khi giải nén, chúng ta thu được một thư mục chứa các file ảnh `.bmp` (thư mục `test`) và một file thực thi Windows `main.exe`.

- Tên bài toán **"B1g_Mac"** gợi ý trực tiếp đến thuật ngữ **MAC times** (Modification, Access, Creation) — hệ thống mốc thời gian lưu trữ của tập tin trên phân vùng NTFS của Windows.

Khi thực hiện phân tích tĩnh (Static Analysis) file thực thi `main.exe` bằng Ghidra, chúng ta phát hiện chương trình sử dụng các hàm Windows API (`GetFileTime`, `SetFileTime`) để can thiệp vào cấu trúc `FILETIME` 64-bit của các file ảnh trong thư mục `test`. Thay vì giấu tin trong dữ liệu ảnh (Steganography), tác giả đã ẩn giấu các byte của Flag trực tiếp vào **phần nano giây (các byte thấp `dwLowDateTime`)** của mốc thời gian tập tin nhằm tránh sự phát hiện của các lệnh liệt kê thông thường trên Linux.

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
---
## Giải pháp
- Do môi trường hệ điều hành Linux hiển thị và làm tròn các mốc thời gian thô của hệ thống file Windows (NTFS FILETIME) khác nhau, việc đọc trực tiếp bằng mắt qua lệnh `ls` hay `exiftool` thông thường sẽ làm mất đi các byte dữ liệu ở phần đuôi nano giây.

- Để giải quyết bài toán này, ta sẽ tận dụng hàm giải mã bằng Binary Patching 

- Vì hàm `decodeBytes` đã được viết sẵn bên trong cấu trúc file nhị phân nhưng không được gọi, chúng ta sẽ tiến hành thay đổi luồng thực thi (Patch) trực tiếp mã máy của file `main.exe`.

- Mục tiêu là đổi lệnh gán `local_14 = 0` thành `local_14 = 1` trong hàm `main`. Cụm mã máy tương ứng `\xc7\x45\xec\x00\x00\x00\x00` (gán bằng 0) sẽ được thay thế bằng `\xc7\x45\xec\x01\x00\x00\x00` (gán bằng 1).

Thực hiện chuỗi lệnh sau trên Kali Linux terminal:

```bash
# 1. Tạo bản sao để thực hiện chỉnh sửa
cp main.exe main_patch.exe

# 2. Sử dụng công cụ sed để ghi đè cấu trúc opcode mã máy
sed -i 's/\xc7\x45\xec\x00\x00\x00\x00/\xc7\x45\xec\x01\x00\x00\x00/g' main_patch.exe

# 3. Tạo một file flag.txt ảo để chương trình không bị crash điều kiện kiểm tra
echo "123456789012345678" > flag.txt

# 4. Thực thi file đã patch thông qua Wine (Lớp tương thích Windows trên Linux)
wine main_patch.exe
```
**Kết quả:** File `main_patch.exe` ép buộc luồng xử lý chạy trực tiếp vào hàm `decodeBytes`. Nó sẽ tự động trích xuất các mốc thời gian NTFS thô chính xác của chuỗi các file `.bmp` và in/nhả trực tiếp ra Flag chính xác đúng định dạng mong muốn.

# Note
- 