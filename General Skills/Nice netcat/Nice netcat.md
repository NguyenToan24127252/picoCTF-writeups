### Bài toán
- Description
    - There is a nice program that you can talk to by using this command in a shell: Additional details will be available after launching your challenge instance.
    - There is a nice program that you can talk to by using this command in a shell: $ nc wily-courier.picoctf.net 63541, but it doesn't speak English...

### Giải
- Kết nối: Dùng ncat (hoặc nc) để kết nối tới server:nc wily-courier.picoctf.net 63541
- Thu thập dữ liệu: Server trả về một danh sách các số thập phân (Decimal) trên nhiều dòng.
- Xử lý bằng Python:
    - Sử dụng sys.stdin.read() để nhận dữ liệu nhiều dòng (multi-line).
    - Sử dụng .split() để tách các số ra khỏi khoảng trắng và dấu xuống dòng.
    - Sử dụng vòng lặp và chr() để chuyển số sang ký tự ASCII.
    - Dùng Ctrl+D để báo hiệu kết thúc nhập liệu (EOF).
- Code giải tối ưu
```
import sys

# Đọc toàn bộ dữ liệu từ Standard Input
data = sys.stdin.read()

# Chuyển đổi dãy số thành chuỗi ký tự
# int(n): chuyển chuỗi "112" thành số 112
# chr(...): chuyển số 112 thành chữ 'p'
flag = "".join([chr(int(n)) for n in data.split()])

print(f"Flag: {flag}")
```
### Note
- Dùng lệnh echo "" | nc wily-courier.picoctf.net 54482 | python3 solve.py > flag.txt
    - echo "": Tạo ra một dòng trống và gửi nó đi. Điều này dùng để "đánh thức" server hoặc giả lập việc nhấn Enter nếu server yêu cầu tương tác ban đầu.

    - | (Pipe thứ nhất): Chuyển dòng trống đó làm đầu vào cho lệnh nc.

    - nc wily-courier.picoctf.net 54482: Kết nối tới server của picoCTF. Nó nhận dòng trống từ echo, gửi đi, sau đó hứng toàn bộ dãy số mà server trả về.

    - | (Pipe thứ hai): Lấy toàn bộ dãy số từ nc và "bơm" thẳng vào chương trình Python của bạn.

    - python3 solve.py: Script của bạn sẽ đọc dữ liệu từ stdin (đầu vào tiêu chuẩn), thực hiện việc chuyển đổi từ số sang ký tự ASCII.

    - lệnh > flag.txt (Redirection): Thay vì in kết quả ra màn hình Terminal, lệnh này điều hướng toàn bộ kết quả cuối cùng và lưu vào file flag.txt.
