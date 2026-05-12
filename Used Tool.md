# CTF used tools

Tổng hợp các công cụ đã cài đặt trên Kali Linux nhằm phục vụ mục đích giải các bài toán **CTF**
---

## 1. QEMU (Quick Emulator)

* **Định nghĩa:** Là một trình mô phỏng và ảo hóa mã nguồn mở. Nó cho phép chạy các chương trình được biên dịch cho một kiến trúc CPU này (như ARM, MIPS) trên một kiến trúc CPU khác (như x86_64).
* **Áp dụng:** Khi gặp các bài CTF có kiến trúc không phải x86 (như các bài ARMssembly trên picoCTF), dùng để thực thi file binary mà không cần phần cứng thật.
* **Cách sử dụng:**
```bash
# Chạy file thực thi ARM64
qemu-aarch64 ./ten_file_binary <doi_so>

```
## 2. Ghidra

* **Định nghĩa:** Một bộ khung công cụ dịch ngược mã nguồn (Reverse Engineering Framework) được phát triển bởi NSA.
* **Áp dụng:** Dùng để phân tích tĩnh (Static Analysis). Ghidra có thể dịch mã máy (Assembly) về mã giả C (Decompiler), giúp người dùng hiểu logic chương trình dễ dàng hơn.
* **Cách sử dụng:**
1. Gõ `ghidra` trong terminal để mở giao diện GUI.
2. Tạo Project mới và Import file cần phân tích.
3. Nhấn vào biểu tượng con rồng để bắt đầu "Auto Analyze".

## 3. GDB (GNU Debugger)

* **Định nghĩa:** Trình gỡ lỗi tiêu chuẩn cho các hệ thống Unix.
* **Áp dụng:** Dùng để phân tích động (Dynamic Analysis). Bạn có thể dừng chương trình tại bất kỳ đâu, xem giá trị thanh ghi, bộ nhớ và điều khiển luồng thực thi.
* **Cách sử dụng:**

```bash
    gdb ./ten_file
    (gdb) break main  # Đặt điểm dừng tại hàm main
    (gdb) run        # Chạy chương trình
    (gdb) info registers # Xem giá trị các thanh ghi
```

## 4. Pwntools
*   **Định nghĩa:** Một thư viện Python cực mạnh được thiết kế dành riêng cho việc viết script khai thác lỗ hổng.
*   **Áp dụng:** Dùng để tự động hóa việc tương tác với chương trình (Local/Remote), chuyển đổi dữ liệu (Endianness), tạo shellcode, hoặc tìm kiếm địa chỉ hàm (ROP).
*   **Cách sử dụng (Trong Python script):**
```python
    from pwn import *
    p = process('./file_binary')
    p.sendline(b'A' * 32)
    print(p.recvall())
```

## 5. Checksec
*   **Định nghĩa:** Một công cụ kiểm tra các cơ chế bảo mật được tích hợp trong file binary.
*   **Áp dụng:** Giúp xác định file có bật các lớp bảo vệ như NX (Non-Executable), Canary (chống tràn buffer), hay PIE (địa chỉ ngẫu nhiên) hay không để đưa ra phương án tấn công.
*   **Cách sử dụng:**
    ```bash
    checksec --file=ten_file
    ```

## 6. Bộ công cụ Biên dịch chéo (Cross-Compile Toolchain)
*   **Thành phần:** `gcc-aarch64-linux-gnu`, `libc6-dev-arm64-cross`.
*   **Định nghĩa:** Là trình biên dịch và các thư viện hỗ trợ tạo ra file thực thi cho kiến trúc ARM64 ngay trên máy tính x86.
*   **Áp dụng:** Dùng để biên dịch các file Assembly `.S` thành file thực thi `.elf` để có thể chạy thử bằng QEMU.
*   **Cách sử dụng:**
    
```bash
    aarch64-linux-gnu-gcc -static file.S -o file_executable
```

## 7. Valgrind

* **Định nghĩa:** Là một bộ khung công cụ (instrumentation framework) dùng để giám sát bộ nhớ, phát hiện lỗi và phân tích hiệu năng của chương trình.
* **Áp dụng:** * **Phát hiện lỗi bộ nhớ:** Tìm kiếm các lỗi như rò rỉ bộ nhớ (memory leaks), truy cập vùng nhớ chưa khởi tạo hoặc tràn bộ nhớ đệm (buffer overflow).
    * **Tấn công kênh bên (Side-channel/Timing Attack):** Trong CTF (như bài `checkpass`), công cụ `cachegrind` của Valgrind cực kỳ hữu ích để đếm chính xác số lượng lệnh thực thi (**Instruction references - Ir**). Khi bạn đoán đúng một ký tự của flag, chương trình sẽ chạy thêm các lệnh kiểm tra cho ký tự tiếp theo, làm tổng số lệnh tăng vọt, giúp bạn "bẻ" từng ký tự một.
* **Cách sử dụng:**

```bash
# Sử dụng công cụ cachegrind để đếm số lệnh thực thi
valgrind --tool=cachegrind ./ten_file_binary <doi_so>

# Xem báo cáo chi tiết về lỗi bộ nhớ
valgrind --leak-check=full ./ten_file_binary