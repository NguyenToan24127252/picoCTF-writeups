### Bài toán
- Description
    - only file keygenme-trial.py

### Giải
- Trong hàm check_key nó xác định:
    - Độ dài: Key phải dài bằng key_full_template_trial, tức là dài 33 ký tự
    - Phần tĩnh (Static): 23 ký tự đầu tiên phải là picoCTF{1n_7h3_kk3y_of_
    - Phần động (Dynamic): 8 ký tự tiếp theo được lấy từ mã băm SHA-256 của username (BENNETT). Tuy nhiên, các vị trí bị đảo lộn
    - Ký tự cuối: Phải là dấu }
- Mã băm SHA-256 của username BENNETT sẽ là một chuỗi Hex dài. Theo check_key, 8 ký tự tiếp theo của key được lấy theo thứ tự index sau:
    - Ký tự 1: Index [4]
    - Ký tự 2: Index [5]
    - Ký tự 3: Index [3]
    - Ký tự 4: Index [6]
    - Ký tự 5: Index [2]
    - Ký tự 6: Index [7]
    - Ký tự 7: Index [1]
    - Ký tự 8: Index [8]
- Chạy script python => KEY
### Note
- Static Key vs Dynamic Key: Trong bảo mật phần mềm, việc kết hợp một phần cố định và một phần thay đổi theo thông tin người dùng là cách phổ biến để tạo License Key cá nhân hóa.
- Hash Function (SHA-256): Bài này minh họa ứng dụng của hàm băm một chiều. Dù hacker biết thuật toán, họ vẫn cần username chính xác để tạo ra key đúng.
- Index Scrambling: Việc đảo lộn thứ tự các ký tự băm ([4, 5, 3, 6...]) là một lớp bảo vệ nhỏ (Security by Obscurity) để gây khó khăn cho người đọc code nếu không nhìn kỹ.