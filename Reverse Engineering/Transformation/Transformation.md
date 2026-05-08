### Bài toán
- Description
    - I wonder what this really is...
enc ''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])

### Giải
- Đọc file enc để lấy chuỗi đã mã hóa.
- Với mỗi ký tự c trong chuỗi đó, ta tách ra làm hai:
    - Ký tự lẻ: chr(ord(c) >> 8)
    - Ký tự chẵn: chr(ord(c) & 0xFF)
- Ghép lại ta sẽ được flag hoàn chỉnh.
