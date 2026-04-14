### Bài toán
Description
Python scripts are invoked kind of like programs in the Terminal...
Can you run ende.py using password.txt to get flag.txt.en?

### Giải
- Dùng lệnh: python3 ende.py -d flag.txt.en 
- Nó đòi mật khẩu thì nhập mật khẩu trong file txt
- Hoặc dùng: python3 ende.py -d flag.txt.en < password.txt   để bơm thẳng mật khẩu từ txt vào script

### Note
- -e (Encode / Encrypt): * Dùng để mã hóa.
Nếu bạn có một file văn bản bình thường (ví dụ flag.txt) và muốn biến nó thành file đã mã hóa (flag.txt.en), bạn sẽ dùng tham số này.

- -d (Decode / Decrypt): * Dùng để giải mã.
Đây là lệnh bạn vừa dùng thành công. Nó yêu cầu script chuyển đổi file đã bị mã hóa (.en) quay ngược lại thành văn bản gốc (Flag) bằng cách sử dụng mật khẩu.

- -h (Help): * Dùng để trợ giúp.
Khi bạn gõ python3 ende.py -h, script sẽ in ra một đoạn hướng dẫn ngắn gọn về cách sử dụng, các tham số cần thiết và thứ tự nhập liệu.