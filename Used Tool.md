# CTF used tools

Tổng hợp các công cụ và thư viện hữu ích đã cài đặt trên Kali Linux nhằm phục vụ mục đích giải các bài toán **CTF**
---
# A. CÁC CÔNG CỤ

## 1. QEMU (Quick Emulator)

* **Định nghĩa:** Là một trình mô phỏng và ảo hóa mã nguồn mở. Nó cho phép chạy các chương trình được biên dịch cho một kiến trúc CPU này (như ARM, MIPS) trên một kiến trúc CPU khác (như x86_64).
* **Áp dụng:** Khi gặp các bài CTF có kiến trúc không phải x86 (như các bài ARMssembly trên picoCTF), dùng để thực thi file binary mà không cần phần cứng thật.
* **Cách sử dụng:**
```bash
# Chạy file thực thi ARM64
qemu-aarch64 ./ten_file_binary <doi_so>
```
---

## 2. Ghidra

* **Định nghĩa:** Một bộ khung công cụ dịch ngược mã nguồn (Reverse Engineering Framework) được phát triển bởi NSA.
* **Áp dụng:** Dùng để phân tích tĩnh (Static Analysis). Ghidra có thể dịch mã máy (Assembly) về mã giả C (Decompiler), giúp người dùng hiểu logic chương trình dễ dàng hơn.
* **Cách sử dụng:**
1. Gõ `ghidra` trong terminal để mở giao diện GUI.
2. Tạo Project mới và Import file cần phân tích.
3. Nhấn vào biểu tượng con rồng để bắt đầu "Auto Analyze".

---

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

---

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
---

## 5. Checksec
*   **Định nghĩa:** Một công cụ kiểm tra các cơ chế bảo mật được tích hợp trong file binary.
*   **Áp dụng:** Giúp xác định file có bật các lớp bảo vệ như NX (Non-Executable), Canary (chống tràn buffer), hay PIE (địa chỉ ngẫu nhiên) hay không để đưa ra phương án tấn công.
*   **Cách sử dụng:**
    ```bash
    checksec --file=ten_file
    ```

---

## 6. Bộ công cụ Biên dịch chéo (Cross-Compile Toolchain)
*   **Thành phần:** `gcc-aarch64-linux-gnu`, `libc6-dev-arm64-cross`.
*   **Định nghĩa:** Là trình biên dịch và các thư viện hỗ trợ tạo ra file thực thi cho kiến trúc ARM64 ngay trên máy tính x86.
*   **Áp dụng:** Dùng để biên dịch các file Assembly `.S` thành file thực thi `.elf` để có thể chạy thử bằng QEMU.
*   **Cách sử dụng:**
    
```bash
    aarch64-linux-gnu-gcc -static file.S -o file_executable
```

---

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
```
---

## 8. Radare2 (r2)

* **Định nghĩa:** Là một khung làm việc (framework) mã nguồn mở cực kỳ mạnh mẽ cho việc dịch ngược và phân tích mã máy thông qua dòng lệnh.
* **Áp dụng:** Tương tự như Ghidra nhưng hoạt động hoàn toàn trên terminal. Radare2 rất nhẹ, nhanh và hỗ trợ script hóa tốt. Nó thường được dùng để phân tích nhanh cấu trúc file, tìm kiếm chuỗi (strings), hoặc patch (sửa đổi) file binary trực tiếp.
* **Cách sử dụng:**

```bash
    r2 ./file_binary       # Mở file
    (r2) aaa               # Tự động phân tích toàn bộ (analyze all)
    (r2) afl               # Liệt kê tất cả các hàm (analyze functions list)
    (r2) pdf @main         # In mã máy của hàm main (print disassembly function)
    (r2) vv                # Mở giao diện đồ họa dạng khối (Visual Mode)
```

---

## 9. Z3-Solver

* **Định nghĩa:** Là một công cụ giải các định lý (Theorem Prover) hiệu năng cao được phát triển bởi Microsoft Research.
* **Áp dụng:** Trong CTF, Z3 là "vũ khí hạng nặng" cho các bài Reversing hoặc Crypto có hệ phương trình phức tạp. Khi bạn tìm thấy logic kiểm tra flag (ví dụ: `flag[0] * 2 + flag[1] == 150`), thay vì giải tay, bạn chỉ cần mô tả các điều kiện cho Z3 và nó sẽ tự tìm ra giá trị của flag.
* **Cách sử dụng (Trong Python script):**

```python
    from z3 import *
    s = Solver()
    x = Int('x')
    y = Int('y')
    s.add(x + y == 10, x > 2, y < 5) # Thêm các điều kiện
    if s.check() == sat:            # Kiểm tra xem có nghiệm không
        print(s.model())            # In ra kết quả
```

---

## 10. Wireshark & Tshark

* **Định nghĩa:** Wireshark là công cụ phân tích giao thức mạng (Packet Sniffer) phổ biến nhất thế giới. Tshark là phiên bản dòng lệnh của Wireshark.
* **Áp dụng:** Dùng trong mảng **Forensics** và **Network**. Giúp trích xuất dữ liệu từ các file lưu lượng mạng (`.pcap`, `.pcapng`), theo dõi các luồng TCP/HTTP để tìm flag bị rò rỉ hoặc khôi phục các file được truyền tải qua mạng (như ảnh, zip, script).
* **Cách sử dụng:**
* **Wireshark:** Gõ `wireshark file.pcap` để mở giao diện GUI, sau đó dùng các bộ lọc như `http`, `tcp.stream eq 5`, hoặc `dns`.
* **Tshark:** Dùng để trích xuất nhanh dữ liệu mà không cần mở GUI.

```bash
    # Trích xuất tất cả các giá trị của một trường cụ thể trong file pcap
    tshark -r file.pcap -T fields -e http.user_agent
```
---

## 11. Binwalk

* **Định nghĩa:** Là một công cụ dòng lệnh chuyên dụng để phân tích, tìm kiếm và trích xuất các tệp tin ẩn hoặc mã thực thi được nhúng bên trong một tệp tin khác dựa trên chữ ký tệp tin (Magic Bytes).
* **Áp dụng:** Cực kỳ phổ biến trong mảng **Forensics**, **Steganography** và **Firmware Analysis**. Khi bạn có một file ảnh đĩa, file firmware router, hoặc thậm chí là một file ảnh `.png` nhưng dung lượng lớn bất thường, Binwalk sẽ quét xem có file `.zip`, `.tar`, hoặc ảnh khác bị nối/giấu ở phía sau hay không.
* **Cách sử dụng:**
```bash
# Kiểm tra cấu trúc và các file bị ẩn bên trong
binwalk file_nghi_van.png

# Tự động trích xuất tất cả các file ẩn tìm thấy ra một thư mục riêng
binwalk -e file_nghi_van.png

# Quét sâu và hiển thị biểu đồ entropy để phát hiện vùng dữ liệu bị mã hóa/nén
binwalk -E file_nghi_van.png
```

---

## 12. Exiftool

* **Định nghĩa:** Là một thư viện và ứng dụng dòng lệnh độc lập viết bằng Perl, chuyên dùng để đọc, ghi và sửa đổi thông tin siêu dữ liệu (Metadata/EXIF) của hàng loạt định dạng tệp tin như hình ảnh, âm thanh, video và tài liệu.
* **Áp dụng:** Dùng trong các bài toán **Forensics**, **OSINT** hoặc **Steganography** sơ cấp. Tác giả đề bài thường giấu Flag hoặc gợi ý quan trọng bên trong các trường thông tin ẩn của file như: Tọa độ GPS nơi chụp ảnh, Tên tác giả (Artist), Nhận xét (Comment), Ngày tạo (Create Date) hoặc phần mềm được dùng để chỉnh sửa.
* **Cách sử dụng:**
```bash
# Hiển thị toàn bộ thông tin Metadata của một file
exiftool anh_chuyen_an.jpg

# Chỉ lọc ra một trường thông tin cụ thể (ví dụ: Tọa độ GPS hoặc Comment)
exiftool anh_chuyen_an.jpg | grep -i "comment"
exiftool -GPSPosition anh_chuyen_an.jpg

# Xóa toàn bộ Metadata của một file để xóa dấu vết
exiftool -all= anh_chuyen_an.jpg
```
---

## 13. Steghide

* **Định nghĩa:** Là một chương trình giấu tin (Steganography) cho phép ẩn một tệp tin bí mật vào trong các tệp tin hình ảnh (`.jpg`, `.bmp`) hoặc âm thanh (`.wav`, `.au`) bằng thuật toán mã hóa nâng cao mà không làm thay đổi kích thước vật lý hay làm giảm chất lượng hiển thị của file gốc.
* **Áp dụng:** Phục vụ trực tiếp cho mảng **Steganography**. Khi gặp một file ảnh `.jpg` hoặc file âm thanh `.wav` mà bạn nghi ngờ có chứa file bí mật bên trong và yêu cầu phải có mật khẩu (Passphrase) để mở, Steghide là công cụ mặc định được nghĩ tới.
* **Cách sử dụng:**

```bash
# Kiểm tra xem file ảnh/âm thanh có chứa dữ liệu ẩn của Steghide không
steghide info file_goc.jpg

# Trích xuất dữ liệu ẩn ra ngoài (sẽ yêu cầu nhập Passphrase nếu có đặt)
steghide extract -sf file_goc.jpg

# Nhúng một file bí mật (secret.txt) vào file ảnh gốc (cover.jpg)
steghide embed -cf cover.jpg -ef secret.txt -p "mat_khau_bao_mat"
```

---

## 14. Stegcracker

* **Định nghĩa:** Là một công cụ dò mã tự động (Brute-force) mã nguồn mở, được thiết kế để bẻ khóa mật khẩu của các tệp tin đã bị giấu tin bằng công cụ Steghide.
* **Áp dụng:** Dùng khi bạn đã xác định được file ảnh có giấu tin bằng `Steghide` nhưng không có mật khẩu. Stegcracker sẽ lấy một danh sách từ điển mật khẩu (Wordlist - như file `rockyou.txt` mặc định trên Kali) và thử liên tục cho đến khi tìm ra mật khẩu đúng để trích xuất file ẩn.
* **Cách sử dụng:**

```bash
# Tiến hành dò mật khẩu file ảnh bằng wordlist rockyou.txt
stegcracker file_bi_an.jpg /usr/share/wordlists/rockyou.txt

# Lưu ý: Nếu stegcracker chạy chậm, bạn có thể cân nhắc dùng 'stegseek' 
# (một bản thay thế viết bằng C++ có tốc độ nhanh gấp hàng ngàn lần)
stegseek file_bi_an.jpg /usr/share/wordlists/rockyou.txt

```
---

## 15. Volatility

* **Định nghĩa:** Là một khung công cụ (Framework) điều tra kỹ thuật số mã nguồn mở cực kỳ mạnh mẽ, chuyên dùng để phân tích dữ liệu trích xuất từ bộ nhớ trong (Memory Forensics / RAM Image).
* **Áp dụng:** Vũ khí tối thượng trong các bài toán **Forensics** nâng cao, nơi đề bài cung cấp một file dump RAM (định dạng `.raw`, `.vmem`, `.dmp`). Volatility giúp điều tra viên khôi phục lại trạng thái của máy tính tại thời điểm dump: xem các tiến trình đang chạy, kết nối mạng, các lệnh cmd đã gõ, cấu trúc file trong cache, thậm chí là trích xuất mật khẩu hoặc flag dạng clear-text nằm trong bộ nhớ.
* **Cách sử dụng (Sử dụng phiên bản Volatility 3 ổn định trên Kali):**

```bash
# Xác định thông tin hệ điều hành của file dump RAM (Profile/Banner)
vol -f dump_ram.raw windows.info

# Liệt kê danh sách các tiến trình đang chạy tại thời điểm dump RAM
vol -f dump_ram.raw windows.pslist

# Xem lịch sử các câu lệnh đã gõ trong Command Prompt (Cmd)
vol -f dump_ram.raw windows.cmdline

# Kết xuất (Dump) toàn bộ file của một tiến trình nghi vấn để phân tích sâu hơn
vol -f dump_ram.raw -o ./output windows.dumpfiles --pid <PID_tien_trinh>
```
---

## 16. Bộ Sleuth Kit (TSK)

* **Định nghĩa:** Là một tập hợp các công cụ dòng lệnh (Command-line tools) mã nguồn mở chuyên sâu dùng để phân tích cấu trúc đĩa và hệ thống tệp tin (File System) ở tầng thấp (như NTFS, FAT32, EXT4) từ các file ảnh đĩa (`.dd`, `.raw`, `.e01`).
* **Áp dụng:** Dùng trong mảng **Forensics** để phân tích sâu cấu trúc đĩa mà không cần mount ổ đĩa vào hệ thống. TSK chia làm nhiều lớp công cụ (bắt đầu bằng các tiền tố đặc trưng) để tương tác với: Khối dữ liệu (`blk`), Siêu dữ liệu hệ thống (`i` - Inode/MFT), Tên file (`f`), và Phân vùng (`mm`). Điểm mạnh của bộ này là khả năng khôi phục file bị xóa và trích xuất chính xác vùng không gian đệm trống (**Slack Space**) của file.
* **Cách sử dụng:**

```bash
# Lớp mm: Xem bảng phân vùng của ổ đĩa để tìm vị trí bắt đầu (Offset) của hệ thống tệp tin
mmls image_o_cung.dd

# Lớp f: Liệt kê danh sách file/thư mục bên trong phân vùng (Dấu * biểu thị file đã bị xóa)
fls -o <offset_phan_vung> image_o_cung.dd

# Lớp i: Xem thông tin chi tiết (Metadata, MACB timestamps) của một inode/MFT hiệu số 1425
istat -o <offset_phan_vung> image_o_cung.dd 1425

# Lớp i: Trích xuất nội dung file thô dựa trên số inode, bao gồm cả vùng Slack Space (-s)
icat -o <offset_phan_vung> -s image_o_cung.dd 1425 > slack_data.txt

```
---

## 17. Autopsy

* **Định nghĩa:** Là một nền tảng điều tra số có giao diện đồ họa (GUI) trực quan, được xây dựng dựa trên nền tảng lõi của các công cụ dòng lệnh thuộc bộ **The Sleuth Kit**.
* **Áp dụng:** Đóng vai trò là trung tâm quản lý ca điều tra (Case Management) cho mảng **Forensics**. Thay vì phải gõ từng lệnh phức tạp của Sleuth Kit, Autopsy tự động hóa việc quét toàn bộ file ảnh đĩa, phân tích cấu trúc tệp tin, lập chỉ mục từ khóa, phân loại hình ảnh/video, hiển thị các file bị xóa, và tự động trích xuất vùng Slack Space thông qua giao diện nhấp chuột trực quan.
* **Cách sử dụng:**

1. Gõ `autopsy` trong terminal của Kali Linux. Hệ thống sẽ khởi chạy một máy chủ cục bộ và cung cấp một đường dẫn URL (hoặc mở ứng dụng GUI tùy phiên bản).
2. Tạo một Case mới (`New Case`) và chọn đường dẫn tới file ảnh đĩa cần điều tra (`Add Data Source`).
3. Lựa chọn các mô-đun phân tích tự động (Ingest Modules) như: *File Type Identification*, *Keyword Search*, *Deleted Files Recovery*.
4. Duyệt cây thư mục bên trái để kiểm tra kết quả, bấm vào tab `Slack Space` ở khung xem dữ liệu phía dưới để kiểm tra các byte dữ liệu ẩn giấu cuối Cluster của file.

---

## 18. SSTV (Python Library / Command-line Tool)

* **Định nghĩa:** Là một công cụ và thư viện mã nguồn mở viết bằng Python, chuyên dụng để giải mã tín hiệu truyền hình quét chậm (**SSTV - Slow Scan Television**) trực tiếp từ dòng lệnh mà không cần giao diện đồ họa hay cấu hình driver âm thanh phức tạp.
* **Áp dụng:** Phục vụ cho mảng **Forensics**, **Audio**, hoặc **Steganography**. Khi đề bài CTF cung cấp một file âm thanh (`.wav`) chứa các tiếng rít và "bíp" rè rè đặc trưng của tín hiệu SSTV, công cụ này giúp bạn ngay lập tức trích xuất ra file ảnh chứa Flag chỉ bằng một dòng lệnh duy nhất, hỗ trợ tự động nhận diện hầu hết các chế độ mã hóa phổ biến (như Robot, Scottie, Martin).
* **Cách sử dụng đầy đủ:**

```bash
# 2. Giải mã cơ bản (Tự động nhận diện Mode và xuất ra file ảnh)
sstv -d file_tin_hieu.wav -o flag_khoi_phuc.png

# 3. Ép kiểu chế độ mã hóa (Chỉ định rõ Mode khi tính năng tự động nhận diện thất bại)
# Các chế độ phổ biến: MartinM1, MartinM2, ScottieS1, ScottieS2, Robot36, Robot72...
sstv -d file_tin_hieu.wav -o flag.png --mode ScottieS1

# 4. Sửa ảnh bị méo/lệch (Tùy chỉnh tần số lấy mẫu - Sampling Rate)
# Đôi khi file âm thanh CTF bị bóp méo tần số khiến ảnh xuất ra bị sọc nghiêng.
# Bạn có thể dùng tham số --rate để ép xung tần số lấy mẫu (mặc định thường là 11025, 22050 hoặc 44100)
sstv -d file_tin_hieu.wav -o flag_thang.png --rate 22050

# 5. Bỏ qua tín hiệu mồi (Strict Verification Bypass)
# Mặc định sstv sẽ tìm kiếm chuỗi tín hiệu "mồi" (calibration header) ở đầu file để bắt đầu dịch.
# Nếu tác giả CTF cắt mất đoạn đầu này, hãy ép công cụ chạy bằng cách bỏ qua kiểm tra:
sstv -d file_bi_cat.wav -o flag.png --no-header

# 6. Xem danh sách tất cả các chế độ mã hóa (SSTV Modes) mà công cụ hỗ trợ
sstv --list-modes
```

> **Mẹo nâng cao cho giải CTF:** Nếu file `.wav` của đề bài có quá nhiều tạp âm (noise) khiến công cụ `sstv` không thể đọc được và trả về lỗi, hãy dùng phần mềm **Audacity** (hoặc lệnh `sox`) trên Kali để lọc nhiễu (Noise Reduction), chuẩn hóa âm lượng (Normalize) về mức `-1dB`, sau đó chạy lại lệnh `sstv` ở trên để lấy ảnh rõ nét nhất.

Dưới đây là nội dung mục **B. CÁCH ÁP DỤNG** được đúc kết từ cẩm nang các công cụ trên, giúp bạn định hình nhanh phản xạ: **"Nhìn thấy loại file/dấu hiệu này $\rightarrow$ bật ngay công cụ đó"** khi thực chiến CTF.

---

# B. CÁCH ÁP DỤNG ĐỐI VỚI TỪNG DẠNG BÀI
### 1. Khi gặp File thực thi hoặc Mã máy (Binary / Assembly / Source Code)

* **File `.S` (Mã nguồn Assembly của các kiến trúc lạ như ARM, MIPS):**
$\rightarrow$ Sử dụng **Bộ công cụ Biên dịch chéo (Cross-Compile Toolchain)** để biên dịch file `.S` thành file thực thi `.elf`.
* **File thực thi kiến trúc không phải x86 (ARM, MIPS, AArch64...):**
$\rightarrow$ Sử dụng **QEMU** để chạy giả lập file binary đó ngay trên Kali Linux.
* **Mọi file thực thi (Linux ELF, Windows EXE) thuộc bài Pwn/Reverse:**
$\rightarrow$ Việc đầu tiên là chạy **Checksec** để kiểm tra các lớp bảo vệ (NX, Canary, PIE), từ đó biết được chương trình có thể bị tấn công bằng kỹ thuật nào (với dụ: tắt NX thì có thể dùng Shellcode, bật NX thì phải dùng ROP).
* **Cần phân tích thuật toán, logic ngầm của File thực thi (Static Analysis):**
$\rightarrow$ Ném file vào **Ghidra** để dịch ngược ra mã giả C cho dễ đọc. Nếu cần check nhanh chuỗi ký tự, cấu trúc hàm trực tiếp trên Terminal thì dùng **Radare2 (r2)**.
* **Cần debug chạy thử, xem thanh ghi, thay đổi luồng thực thi (Dynamic Analysis):**
$\rightarrow$ Chạy file bằng **GDB** (kết hợp với các giao diện như GEF/Pwndbg) để đặt các điểm dừng (breakpoint).
* **Cần viết Script tự động gửi payload khai thác (Local/Remote):**
$\rightarrow$ Sử dụng thư viện **Pwntools** trong Python để quản lý kết nối và đóng gói dữ liệu cấu trúc lớn.
* **Bài toán cho một chương trình kiểm tra mật khẩu (Checkpass/Validator) rất dài:**
$\rightarrow$ Hãy dùng **Valgrind (Cachegrind)** để đo số lượng lệnh thực thi `Ir`. Nếu số lệnh tăng lên khi bạn thay đổi một ký tự, chứng tỏ ký tự đó đã đúng (Tấn công kênh bên - Timing Attack).

### 2. Khi gặp Hệ phương trình hoặc Logic toán phức tạp (Crypto / Reverse)

* **Logic chương trình chứa hàng chục điều kiện ràng buộc giữa các ký tự của Flag:**
$\rightarrow$ Đừng giải tay hay viết vòng lặp brute-force mất thời gian. Hãy nạp toàn bộ các điều kiện toán học đó vào **Z3-Solver** bằng Python để nó tự giải và trả về Flag chính xác.

### 3. Khi gặp File Lưu lượng mạng (Network Forensics)

* **File mở rộng `.pcap`, `.pcapng`:**
$\rightarrow$ Sử dụng **Wireshark** (Giao diện GUI) để lọc gói tin, theo dõi các luồng TCP stream. Nếu file dung lượng quá lớn hoặc cần viết script cào dữ liệu tự động (như lấy toàn bộ chuỗi User-Agent), hãy dùng **Tshark** trên Terminal.

### 4. Khi gặp File dữ liệu ẩn giấu (Forensics / Steganography)

* **Một file bất kỳ (Ảnh, Nhạc, Tài liệu) có dung lượng lớn bất thường hoặc nghi ngờ bị giấu hàng:**
$\rightarrow$ Dùng **Binwalk** để quét các chữ ký tệp tin (Magic Bytes). Nếu phát hiện có file ẩn bên trong (như một file `.zip` nằm cuối file `.png`), dùng lệnh `binwalk -e` để trích xuất ra.
* **File ảnh (`.jpg`, `.png`), file âm thanh hoặc tài liệu thông thường:**
$\rightarrow$ Chạy **Exiftool** để kiểm tra toàn bộ Metadata. Đôi khi tác giả giấu Flag ngay trong các trường thông tin như `Comment`, `Artist`, hoặc tọa độ `GPS`.
* **File ảnh `.jpg`, `.bmp` hoặc file âm thanh `.wav` nghi có mật khẩu:**
$\rightarrow$ Sử dụng **Steghide** để kiểm tra cấu trúc ẩn hoặc trích xuất file bí mật. Nếu đề bài yêu cầu Passphrase nhưng không cho, hãy dùng **Stegcracker** (hoặc **Stegseek**) kết hợp với danh sách từ điển `rockyou.txt` để bẻ khóa.
* **File âm thanh `.wav` chứa các tiếng "bíp, rít" rè rè kỳ lạ:**
$\rightarrow$ Đây là định dạng truyền hình quét chậm. Sử dụng công cụ **SSTV** (Python) để giải mã trực tiếp file âm thanh đó thành file ảnh chứa Flag trên màn hình terminal.

### 5. Khi gặp File cấu trúc hệ thống (Disk / Memory Forensics)

* **File Dump bộ nhớ RAM (`.raw`, `.vmem`, `.dmp`):**
$\rightarrow$ Sử dụng **Volatility** để dựng lại lịch sử máy tính: kiểm tra các câu lệnh cmd đã gõ, các tiến trình đang chạy ngầm hoặc trích xuất các file nằm trong bộ nhớ cache của RAM.
* **File ảnh đĩa, phân vùng ổ cứng (`.dd`, `.raw`, `.e01`):**
$\rightarrow$ Sử dụng **Bộ Sleuth Kit (TSK)** trên Terminal để phân tích sâu ở tầng thấp (kiểm tra bảng phân vùng bằng `mmls`, tìm file xóa bằng `fls`, trích xuất vùng khoảng trống `Slack Space` bằng `icat`).
$\rightarrow$ Nếu muốn có giao diện trực quan, quản lý ca điều tra theo dạng nhấp chuột và tự động phân loại hình ảnh/từ khóa, hãy import file ảnh đĩa đó vào **Autopsy**.