### Bài toán
- Description
    - Can you get the flag?
Reverse engineer this Python program.

### Giải
- Phân tích mã nguồn:
    - Cơ chế: Chương trình sử dụng một khóa tĩnh (key_str) để giải mã một đoạn dữ liệu (payload) đã được mã hóa bằng Fernet. Sau khi giải mã thành công, kết quả (plain) sẽ được thực thi trực tiếp bằng lệnh exec().
    - Khóa (Key): correctstaplecorrectstaplecorrec (được chuyển sang định dạng Base64 để phù hợp với yêu cầu của Fernet).
    - Lệnh thực thi: Lệnh exec(plain.decode()) cho thấy Flag hoặc logic in Flag nằm ngay bên trong dữ liệu bị mã hóa.
- Thay dòng exec(plain.decode()) bằng: print(plain.decode())
### Note
- Mã hóa Fernet: Đây là một tiêu chuẩn mã hóa đối xứng sử dụng thuật toán AES trong chế độ CBC và HMAC để xác thực dữ liệu.
- Nguy hiểm của lệnh exec(): Trong Reverse Engineering, lệnh exec() thường được dùng để che giấu logic thực tế (obfuscation). Việc thay thế exec() bằng print() là kỹ thuật cơ bản để "lột trần" lớp vỏ bọc này.
- Xử lý Base64: Thư viện Fernet yêu cầu khóa phải được định dạng Base64 (32 bytes). Việc chuyển đổi key_str.encode() sang Base64 là bước chuẩn bị bắt buộc.