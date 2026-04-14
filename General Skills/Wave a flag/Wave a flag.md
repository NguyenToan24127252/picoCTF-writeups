### Bài toán
- Description
    - Can you invoke help flags for a tool or binary? This program has extraordinarily helpful information...warm

### Giải
- Để chạy một file binary (mã máy) trên Linux và xem hướng dẫn, thực hiện 3 bước chuẩn:
    - file warm: Kiểm tra định dạng file (xác nhận là ELF executable).
    - chmod +x warm: Cấp quyền thực thi cho file (vì mặc định file tải về thường bị chặn chạy).
    - ./warm -h: Chạy file với đối số -h (help) để yêu cầu chương trình hiển thị trợ giúp/flag.

### Note
- Trong Linux, khi bạn gõ một lệnh, cấu trúc thường là:  command [options/flags] [arguments] 
1. Arguments
- Là các giá trị bạn truyền vào chương trình để nó biết cần phải làm việc với cái gì
    - VD: lệnh cat password.txt, thì password.txt là một đối số
2. Flags/Options
- Là một loại đối số đặc biệt, thường bắt đầu bằng dấu gạch ngang (- hoặc --), dùng để thay đổi hành vi của chương trình.
    - Short flag (Cờ ngắn): Dùng một dấu gạch ngang và một chữ cái. Ví dụ: -h, -v, -d.
    - Long flag (Cờ dài): Dùng hai dấu gạch ngang và một từ. Ví dụ: --help, --verbose, --decrypt.
