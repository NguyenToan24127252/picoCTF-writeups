# Bài toán
- Description
    - Matryoshka dolls are a set of wooden dolls of decreasing size placed one inside another. What's the final one? Image: dolls.jpg

# Giải
- Sử dụng tool binwalk để quét và giải nén file ẩn trong dolls.jpg:
```
┌──(kali㉿kali)-[/mnt/hgfs/picoCTF-writeups/Forensics/Matryoshka doll]
└─$ binwalk dolls.jpg

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 594 x 1104, 8-bit/color RGBA, non-interlaced
3226          0xC9A           TIFF image data, big-endian, offset of first image directory: 8
272492        0x4286C         Zip archive data, at least v2.0 to extract, compressed size: 378933, uncompressed size: 383920, name: base_images/2_c.jpg
651591        0x9F147         End of Zip archive, footer length: 22
```
- Thấy tại offset 272492 có chứa 1 file ảnh tiếp theo là base_images/2_c.jpg
- Cứ tiếp tục tiến hành giải nén các file jpg binwalk -e <file>.jpg cho tới khi thấy => flag.txt
# Note
## 1. Nhóm lệnh Quét và Phân tích (Scanning & Analysis)
Đây là nhóm lệnh cơ bản nhất dùng để đọc cấu trúc bên trong của một file mà không làm thay đổi hay trích xuất dữ liệu.
* **Quét cơ bản (Mặc định):**
```bash
binwalk <tên_file>
```
*Ý nghĩa:* Quét file và hiển thị các thành phần (signatures) tìm thấy cùng với vị trí Offset (thập phân và lục phân).
* **Chỉ quét các chữ ký số (Signatures) cụ thể:**
```bash
binwalk -I <tên_file>
```
*Ý nghĩa:* Chạy quét nhưng bỏ qua các kết quả trùng lặp hoặc không chắc chắn (hiệu quả khi file có quá nhiều thông tin rác).
* **Tìm kiếm chuỗi văn bản cụ thể (String Search):**
```bash
binwalk -R "\x74\x65\x73\x74" <tên_file>
```
*Ý nghĩa:* Tìm kiếm một chuỗi byte cụ thể (trong ví dụ là chuỗi từ "test" dạng hex) trong file nhị phân.
---
## 2. Nhóm lệnh Trích xuất và Bóc tách (Extraction)

Nhóm lệnh này giúp bạn "mổ xẻ" file, tự động lấy các file bị ẩn (như file zip, png, elf, lzma...) ra một thư mục riêng.

* **Tự động trích xuất mọi thứ tìm thấy:**
    
```bash
binwalk -e <tên_file>
# Hoặc:
binwalk --extract <tên_file>
```
*Ý nghĩa:* Tự động bóc tách tất cả các tệp tin hợp lệ dựa trên quy tắc cấu hình mặc định và lưu vào thư mục `_<tên_file>.extracted`.

*   **Trích xuất cưỡng bức (Force Extraction):**
    
```bash
binwalk -D='.*' <tên_file>
```
*Ý nghĩa:* Ép `binwalk` trích xuất **tất cả** các loại chữ ký tệp tin mà nó nhận diện được, kể cả những loại không có trong quy tắc cấu hình mặc định của tham số `-e`.

*   **Trích xuất chỉ một loại file cụ thể:**
    
```bash
binwalk -D='png image:png' <tên_file>
```
*Ý nghĩa:* Chỉ trích xuất các file định dạng PNG có trong mục tiêu.
---
## 3. Nhóm lệnh Phân tích Entropy (Entropy Analysis)
Phân tích Entropy giúp bạn phát hiện xem file nhị phân có bị mã hóa (Encryption) hoặc bị nén (Compression) hay không. Điểm số Entropy càng gần `1.0` chứng tỏ dữ liệu khu vực đó có độ xáo trộn cực cao (khả năng cao là bị mã hóa/nén).

* **Quét và vẽ biểu đồ đồ họa (Nếu terminal hỗ trợ):**
```bash
binwalk -E <tên_file>
```
*Ý nghĩa:* Tính toán và hiển thị biểu đồ Entropy của file theo từng phân đoạn.
* **Chỉ quét Entropy mà không quét chữ ký file:**
```bash
binwalk -J <tên_file>
```
*Ý nghĩa:* Tiết kiệm thời gian bằng cách bỏ qua việc tìm kiếm signature, chỉ tập trung đo lường độ xáo trộn dữ liệu (Entropy).
---

## 4. Nhóm lệnh So sánh File (Diffing)

Dùng khi bạn có nhiều phiên bản firmware hoặc nhiều file muốn so sánh sự khác biệt ở mức byte.

* **So sánh mã Hex của hai hoặc nhiều file:**

```bash
binwalk -W <file_1> <file_2> <file_3>
```
*Ý nghĩa:* Hiển thị màn hình so sánh mã Hex (Hexdump). Những phần dữ liệu **giống nhau** giữa các file sẽ được tô **màu xanh lá**, phần **khác nhau** sẽ tô **màu đỏ**. Rất hữu ích để tìm đoạn code bị vá (patch).

---

## 5. Nhóm lệnh Nâng cao & Tùy chỉnh dòng lệnh

* **Quét từ một vị trí Offset cụ thể:**
    
```bash
binwalk -o 0x4286C <tên_file>
```
*Ý nghĩa:* Bỏ qua đoạn đầu, chỉ bắt đầu quét file từ vị trí byte thứ `0x4286C`.
* **Giới hạn số lượng byte cần quét:**
    
```bash
binwalk -l 10000 <tên_file>
```
*Ý nghĩa:* Chỉ quét đúng `10000` bytes đầu tiên của file rồi dừng lại.

* **Hiển thị thông tin Debug chi tiết:**
    
```bash
binwalk -v <tên_file>
```
*Ý nghĩa:* Chế độ Verbose, hiển thị chi tiết quá trình `binwalk` quét qua từng plugin và luật (rules). Thêm `-vv` để hiển thị chi tiết hơn nữa.

---

## 💡 Mẹo kết hợp các lệnh thường dùng trong CTF / Pentest

```bash
# Quét, tự động giải nén VÀ hiển thị chi tiết quá trình chạy
binwalk -ev <tên_file>

# Quét Entropy kết hợp tìm kiếm Signature để xem vùng nào bị mã hóa
binwalk -EE <tên_file>

# Ép trích xuất toàn bộ dữ liệu từ một offset nghi vấn cụ thể
binwalk -D='.*' -o 0x1000 <tên_file>

```
