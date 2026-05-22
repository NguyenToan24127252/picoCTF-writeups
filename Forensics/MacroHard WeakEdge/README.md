# Bài toán
- Description
    - I've hidden a flag in this file. Can you find it?
Forensics_is_fun.pptm

# Giải

* **Phân tích ban đầu:**
* Định dạng file được cung cấp là .pptm (Microsoft PowerPoint Macro-Enabled Presentation). Thực chất, các file Office hiện đại đều là các file nén dạng ZIP chứa cấu trúc thư mục XML và tài nguyên bên trong.


* **Các bước thực hiện:**
1. **Chuyển đổi định dạng:** Tiến hành đổi đuôi file từ Forensics_is_fun.pptm sang Forensics_is_fun.zip và giải nén bằng công cụ có sẵn trên Linux hoặc lệnh unzip.
2. **Tìm kiếm file ẩn:** Sau khi giải nén, di chuyển vào cấu trúc thư mục và phát hiện một file văn bản đáng nghi có tên là hidden nằm sâu trong đường dẫn:
./ppt/slideMasters/hidden
3. **Kiểm tra nội dung:** Sử dụng lệnh cat hidden để đọc file, ta thu được một chuỗi ký tự được chèn rất nhiều dấu cách ở giữa:
Z m x h Z z o g c G l j b 0 N U R n t E M W R f d V 9 r b j B 3 X 3 B w d H N f c l 9 6 M X A 1 f Q
4. **Làm sạch và giải mã:** Chuỗi ký tự trên có dạng mã hóa Base64 nhưng bị phân tách bởi khoảng trắng để tránh các lệnh quét strings thông thường. Ta sử dụng lệnh tr -d ' ' để loại bỏ dấu cách, sau đó đẩy qua base64 -d để giải mã.


* **Lệnh khai thác cuối cùng (One-liner):**
```bash
cat ppt/slideMasters/hidden | tr -d ' ' | base64 -d
```

# Note

* **Bẫy Obfuscation (Làm rối chuỗi):**
* Tác giả cố tình chèn khoảng trống giữa các ký tự (Z m x h...) để vô hiệu hóa các lệnh quét chuỗi thô thông thường như strings | grep "pico".
* *Kinh nghiệm:* Nếu grep từ khóa chính không ra, hãy thử quét các từ khóa ngắn hơn (như p i c o), hoặc tìm kiếm theo định dạng mã hóa (Regex cho Base64, Hex) thay vì tìm text thuần.


* **Bản chất của file Office (OpenXML):**
* Tất cả các file có đuôi kết thúc bằng chữ **x** hoặc **m** (.docx, .xlsx, .pptx, .pptm) bản chất đều là một file nén ZIP.
* *Kinh nghiệm:* Bước đầu tiên khi nhận được các file này là luôn luôn dùng lệnh file để kiểm tra, sau đó đổi đuôi sang .zip hoặc dùng unzip để "mổ xẻ" cấu trúc bên trong.


* **Các "tọa độ" giấu hàng thường gặp trong PowerPoint:**
* ppt/slideMasters/: Nơi chứa các slide master (slide cấu trúc nền). Rất lý tưởng để giấu các file cấu hình ẩn hoặc text trùng màu nền.
* ppt/media/: Nơi chứa hình ảnh, âm thanh. Cần kiểm tra xem có kỹ thuật giấu tin trong ảnh (Steganography) hay không.
* ppt/vbaProject.bin: Nơi chứa mã nguồn Macro (VBA). Với file có đuôi .pptm như bài này, luôn phải dùng công cụ olevba (trong bộ oletools) để phân tích xem có code độc hại hoặc chuỗi ẩn được thực thi khi mở file không.


* **Tận dụng tối đa Linux CLI:**
* Nên thuần thục các lệnh xử lý chuỗi nhanh như tr -d ' ' (xóa khoảng trắng), rev (đảo ngược chuỗi), xxd (xem mã hex) và kết hợp luồng pipe (|) để giải mã nhanh mà không cần dùng đến các công cụ online như CyberChef.