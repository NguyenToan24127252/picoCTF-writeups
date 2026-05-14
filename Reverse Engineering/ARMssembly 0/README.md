### Bài toán
- Description
    - What integer does this program print?
Flag format: picoCTF{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be picoCTF{0055aabb})
Use arguments a and b: 2593949075 and 2233560849
File: chall.S

### Giải
- Cách 1: phân tích
    - Trong ARM64, khi gọi hàm main(argc, argv), các tham số từ dòng lệnh sẽ được xử lý:
        - Đoạn code lấy argv[1] (đối số thứ nhất) truyền vào atoi để chuyển thành số nguyên, lưu vào w19.
        - Tiếp theo lấy argv[2] (đối số thứ hai) truyền vào atoi, kết quả trả về nằm ở w0.
        - Sau đó, nó chuẩn bị gọi hàm func1:
            - mov w1, w0: Gán giá trị b vào thanh ghi w1.
            - mov w0, w19: Gán giá trị a vào thanh ghi w0.
            - bl func1: Gọi hàm func1(a, b).
    - Phân tích hàm func1:
    ```
    func1:
        sub     sp, sp, #16     // Tạo không gian stack
        str     w0, [sp, 12]    // Lưu a (2593949075) vào stack
        str     w1, [sp, 8]     // Lưu b (2233560849) vào stack
        
        ldr     w1, [sp, 12]    // Load lại a vào w1
        ldr     w0, [sp, 8]     // Load lại b vào w0
        
        cmp     w1, w0          // So sánh a và b (2593949075 và 2233560849)
        bls     .L2             // Nếu a <= b (Branch if Lower or Same), nhảy đến .L2
        
        ldr     w0, [sp, 12]    // Nếu a > b: Load a vào w0 để trả về
        b       .L3             // Nhảy đến kết thúc
        
    .L2:
        ldr     w0, [sp, 8]     // Nếu a <= b: Load b vào w0 để trả về
        
    .L3:
        add     sp, sp, 16      // Dọn dẹp stack
        ret                     // Trả về giá trị trong w0
    ```
    - Kết luận logic của hàm: Hàm này đơn giản là so sánh hai số và trả về số lớn hơn => func1 trả về 2593949075 chuyển sang hex (no 0x) thành 9a9c8593 => FLAG
- Cách 2: chạy chương trình = qemu
```
┌──(kali㉿kali)-[/mnt/hgfs/picoCTF-writeups/Reverse Engineering/ARMssembly 0]
└─$ # 1. Biên dịch lại với cờ -static
aarch64-linux-gnu-gcc chall.S -o chall_run -static

# 2. Chạy lại bằng QEMU
qemu-aarch64 ./chall_run 2593949075 2233560849
Result: 2593949075
                                                                                           
                                                                                                                                                                                    
┌──(kali㉿kali)-[/mnt/hgfs/picoCTF-writeups/Reverse Engineering/ARMssembly 0]
└─$ python3 -c "print(f'{2593949075:08x}')"
9a9c8593

```
### Note
- QEMU (viết tắt của Quick Emulator) là một phần mềm mô phỏng và ảo hóa mã nguồn mở cực kỳ mạnh mẽ. Nó cho phép tôi chạy một hệ điều hành hoặc một chương trình được thiết kế cho kiến trúc máy tính này (ví dụ: ARM) ngay trên một máy tính có kiến trúc khác (ví dụ: x86/Intel của tôi).
- Hỗ trợ:
    - Phân tích mã độc (Malware Analysis): tôi có thể chạy các mẫu virus dành cho các thiết bị IoT (thường dùng chip ARM hoặc MIPS) trong một môi trường bị cô lập hoàn toàn để xem nó làm gì.
    - Reverse Engineering: Như bài tập tôi vừa làm, QEMU giúp thực thi các file binary của router, camera, hoặc thiết bị nhúng ngay trên laptop của mình để debug.
    - Hỗ trợ Debug cực tốt: QEMU có tích hợp sẵn GDB server. tôi có thể dùng GDB trên máy thật để "step through" (chạy từng dòng) mã nguồn của một chương trình ARM đang chạy bên trong QEMU.