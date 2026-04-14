import sys

print("Dán dãy số vào đây (sau đó nhấn Ctrl+D để kết thúc):")

# sys.stdin.read() sẽ đọc tất cả các dòng bạn dán vào
data = sys.stdin.read()

# Chuyển đổi
try:
    numbers = data.split()
    flag = "".join([chr(int(n)) for n in numbers])
    print(f"\nFlag của bạn là: {flag}")
except ValueError:
    print("\nLỗi: Có ký tự không phải là số trong dữ liệu bạn nhập.")
