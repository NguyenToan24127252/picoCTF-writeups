### Bài toán
- Description
```
Can you get the flag?
Download this binary.
Here's the test drive instructions:
$ chmod +x gdbme
$ gdb gdbme
(gdb) layout asm
(gdb) break *(main+99)
(gdb) run
(gdb) jump *(main+104)
```
### Giải
- Cách 1: giải như hướng dẫn trên 
- Cách 2: giải = phần mềm ghidra
    - Vào hàm main: 
        ```
        undefined8 main(void)

        {
        char *__s;
        long in_FS_OFFSET;
        undefined8 local_38;
        undefined8 local_30;
        undefined8 local_28;
        undefined8 local_20;
        undefined1 local_18;
        long local_10;
        
        local_10 = *(long *)(in_FS_OFFSET + 0x28);
        local_38 = 0x4c75257240343a41;
        local_30 = 0x4362383846336235;
        local_28 = 0x6030624760433530;
        local_20 = 0x4e32676662346668;
        local_18 = 0;
        sleep(100000);
        __s = (char *)rotate_encrypt(0,&local_38);
        fputs(__s,stdout);
        putchar(10);
        free(__s);
        if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                            /* WARNING: Subroutine does not return */
            __stack_chk_fail();
        }
        return 0;
        }
        ```
    - Các biến local_38 đến local_18: Đây chính là nơi chứa chuỗi Flag đã bị mã hóa. ta thấy chúng được gán các giá trị Hex như 0x4c752572.... Trong kiến trúc Little Endian, các chuỗi này sẽ được đọc ngược lại.
    - Lệnh sleep(100000): Chương trình sẽ dừng lại 100,000 giây (hơn 27 tiếng). Đây là lý do nếu ta chạy file bình thường, ta sẽ không bao giờ thấy Flag hiện ra.
    - Lệnh rotate_encrypt(0, &local_38): Sau khi "ngủ" dậy, chương trình mới bắt đầu giải mã chuỗi hex ở trên và lưu vào biến __s.
    - Lệnh fputs(__s, stdout): In Flag đã giải mã ra màn hình.  
    - Đảo byte local_38, local_30, local_28, local_20 
    - sau khi có chuỗi mở hàm rotate_encrypt để xem dùng gì để giải mã nó:
    ```
    char * rotate_encrypt(undefined8 param_1,char *param_2)

    {
    char cVar1;
    char *__s;
    size_t sVar2;
    ulong local_20;
    
    __s = strdup(param_2);
    sVar2 = strlen(__s);
    for (local_20 = 0; local_20 < sVar2; local_20 = local_20 + 1) {
        if ((' ' < __s[local_20]) && (__s[local_20] != '\x7f')) {
        cVar1 = (char)(__s[local_20] + 0x2f);
        if (__s[local_20] + 0x2f < 0x7f) {
            __s[local_20] = cVar1;
        }
        else {
            __s[local_20] = cVar1 + -0x5e;
        }
        }
    }
    return __s;
    }

    ```
    - Nhìn vào thấy: Nhận diện ROT47 qua hằng số dịch chuyển 47 (0x2f) và phép toán bù trừ trên dải 94 (0x5e) ký tự ASCII khả dụng.
    - Lấy chuỗi giải nó = ROT47 ra FLAG
### Note
- Kỹ thuật Anti-Analysis bằng hàm sleep() - Trong thực tế, các phần mềm độc hại (Malware) thường sử dụng các hàm gây trễ như sleep() để làm nản lòng người phân tích hoặc đánh lừa các hệ thống kiểm thử tự động (Sandbox).
    - Mục tiêu: Khiến chương trình tiêu tốn quá nhiều thời gian thực thi, dẫn đến việc Sandbox tự động đóng lại trước khi hành vi độc hại (hoặc trong bài này là việc in Flag) kịp diễn ra.
    - Cách vượt qua: Chúng ta có thể dùng trình gỡ lỗi (GDB) để nhảy qua (jump), hoặc sử dụng Ghidra để chỉnh sửa mã máy (Patching) lệnh sleep thành lệnh NOP (No Operation).

- Kiến trúc lưu trữ Little Endian
    - Các giá trị như local_38 = 0x4c75257240343a41 được lưu trữ dưới dạng Little Endian trên kiến trúc x86_64.
    - Nguyên tắc: Byte thấp nhất (Least Significant Byte) sẽ được lưu ở địa chỉ bộ nhớ thấp nhất.
    - Hệ quả: Khi đọc các giá trị Hex này dưới dạng chuỗi ký tự (String), chúng ta phải đảo ngược thứ tự các cặp byte (ví dụ: 41 là byte cuối cùng trong số Hex nhưng lại là ký tự đầu tiên của chuỗi).

- Bố cục ngăn xếp (Stack Layout) và Ghép chuỗi
    - Trong Ghidra, ta thấy hàm rotate_encrypt(0, &local_38) chỉ nhận địa chỉ của biến đầu tiên.
    - Lý thuyết: Các biến cục bộ local_38, local_30, local_28, local_20 được trình biên dịch đặt nằm liên tiếp nhau trên ngăn xếp (Stack).
    - Kỹ thuật: Vì không có ký tự kết thúc chuỗi (NULL byte) ở giữa các biến này, hàm giải mã sẽ đọc một mạch từ local_38 xuyên qua các biến tiếp theo cho đến khi gặp local_18 = 0. Đây là lý do tại sao chúng ta phải ghép tất cả các giá trị Hex lại mới có thể giải mã được Flag hoàn chỉnh.

- Cơ chế bảo vệ Stack Canary
    - Dòng code local_10 = *(long *)(in_FS_OFFSET + 0x28); và hàm __stack_chk_fail() đại diện cho cơ chế bảo vệ Stack Canary.
    - Cơ chế: Một giá trị ngẫu nhiên (Canary) được đặt vào Stack trước khi hàm thực thi. Trước khi hàm kết thúc, chương trình sẽ kiểm tra xem giá trị này có bị thay đổi không.
    - Ý nghĩa: Nếu ta cố tình Patch file hoặc thực hiện tấn công tràn bộ nhớ (Buffer Overflow), giá trị này sẽ bị sai lệch và chương trình sẽ tự ngắt ngay lập tức để bảo vệ hệ thống.

- Thuật toán ROT47 và Tính đối xứng
    - Hàm rotate_encrypt trong bài thực chất là ROT47.
    - Đặc điểm: ROT47 sử dụng bảng mã ASCII từ ký tự ! (33) đến ~ (126).
    - Tính đối xứng: Vì khoảng cách dịch chuyển (47) đúng bằng một nửa tổng số ký tự khả dụng (94), nên việc áp dụng thuật toán ROT47 lên một chuỗi đã mã hóa sẽ trả về chính văn bản gốc ban đầu. Điều này cho phép một hàm duy nhất đóng vai trò của cả bộ mã hóa và bộ giải mã.