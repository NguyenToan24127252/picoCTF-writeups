### Bài toán
- Description
    - Can you open this safe?
I forgot the key to my safe but this program is supposed to help me with retrieving the lost key. Can you help me unlock my safe?
Put the password you recover into the picoCTF flag format like:
picoCTF{password}

### Giải
- Chương trình yêu cầu người dùng nhập mật khẩu, sau đó mã hóa chuỗi nhập vào bằng Base64 và so sánh với một chuỗi đã được mã hóa cứng trong hàm openSafe.
- Hàm encoder.encodeToString(key.getBytes()): Chuyển mật khẩu người dùng nhập thành chuỗi Base64 và openSafe(String password): Kiểm tra chuỗi đã mã hóa với giá trị mục tiêu.
- echo "chuỗi" | base64 -d
