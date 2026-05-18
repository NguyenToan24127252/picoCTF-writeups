# Bài toán
- Description
    - Revisit the last transmission. We think this transmission contains a hidden message. There are also some clues clue 1, clue 2, clue 3.

# Giải
- Tham khảo trên mạng thì bài này là bài tiếp theo của mOOnwalk -> ta sẽ dùng sstv để decode các file wav sang file ảnh png
- Có được 4 file ảnh thì thấy trong messages.png có flag thử nộp: picoCTF{beep_boop_im_in_space} thì sai nghĩa là nó còn giấu sâu nữa trong message
- Có thể người ta dùng steghide để giấu cờ trong message -> ta cần tìm mật khẩu và sau khi mở các file ảnh clue ta thấy password nằm trong clue1.png: hidden_stegosaurus
- chạy:
```
┌──(kali㉿kali)-[/mnt/hgfs/picoCTF-writeups/Forensics/m00nwalk2]
└─$ steghide extract -sf message.wav -p hidden_stegosaurus
wrote extracted data to "steganopayload12154.txt".
```
- Flag nằm trong file txt

# Note

### 1. Nhận diện tín hiệu SSTV (Slow Scan Television)

* **Dấu hiệu bài toán:** Thử thách có bối cảnh không gian/vũ trụ (như chuỗi bài `m00nwalk`), dữ liệu cung cấp là file âm thanh `.wav` thô (PCM 16-bit Mono) chứa các chuỗi âm thanh "tít tít, rè rè" liên tục với tần số thay đổi rõ rệt khi quan sát bằng phổ tần (Spectrogram).
* **Bản chất công nghệ:** SSTV mã hóa từng điểm ảnh (pixel) và xung dịch dòng (sync pulse) thành các tần số âm thanh cơ bản (Hz). Công cụ `sstv` đóng vai trò giải mã các tần số này để vẽ lại thành ảnh tĩnh (`.png`/`.jpg`).

### 2. Kỹ thuật "Giấu tin lồng nhau" (Nested Steganography)

* Các bài CTF Forensics nâng cao thường áp dụng kỹ thuật giấu tin nhiều lớp: **SSTV (giấu ảnh trong âm thanh) $\rightarrow$ Steghide (giấu file trong âm thanh bằng mật mã)**.
* **Cạm bẫy Flag giả (Honey-pot / Fake Flag):** Luôn cảnh giác với các chuỗi ký tự có dạng flag hiển thị quá lộ liễu ở lớp ngoài cùng (như chuỗi `picoCTF{beep_boop_im_in_space}` trên file `message.png`). Tác giả cố tình đặt flag giả để bẫy người chơi lười phân tích các file manh mối (`clue`).

### 3. Quy trình khai thác với Steghide

* `steghide` là công cụ giấu tin kinh điển trong ảnh (`.jpg`, `.bmp`) hoặc âm thanh (`.wav`, `.au`) dựa trên thuật toán thay đổi các bit dữ liệu mà không làm suy giảm đáng kể chất lượng file gốc.
* Khi bài toán cho nhiều file `clue` đi kèm, cấu trúc khai thác luôn là: **Giải mã Clue $\rightarrow$ Tìm Password $\rightarrow$ Trích xuất payload thực sự từ file gốc**.

### 4. Lệnh Kali Linux cần nhớ cho dạng bài này

* **Decode SSTV:** `sstv -d <input.wav> -o <output.png>`
* **Trích xuất Steghide:** `steghide extract -sf <file_gốc.wav> -p <password>`