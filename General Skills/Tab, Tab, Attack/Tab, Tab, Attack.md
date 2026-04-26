### Bài toán
- Description
    - Can you look at the data in this binary? The bash script might help!
static, ltdis.sh

### Giải
- B1: Cấp quyền thực thi cho script:
```
chmod +x ltdis.sh
```
- B2: Chạy script với đối số là file binary static
```
./ltdis.sh static
```
- Sau khi ra 2 file thì dùng lệnh grep để tìm cờ:
```
grep "picoCTF" static.ltdis.strings.txt
```
### Note
- Bash script là một tệp văn bản chứa một loạt các lệnh Linux được viết sẵn. Thay vì bạn phải gõ từng lệnh một trên Terminal, bạn chỉ cần chạy file script này và nó sẽ tự động thực hiện toàn bộ các bước bên trong. Với đuôi file thường là .sh
- File ltdis.sh sẽ thường dùng để:
    - Strings: xuất các chuỗi văn bản tìm thấy trong file static ra txt
    - Disassemble: sử dụng công cụ objdump để dịch mã máy 0101 của file static sang mã Assembly (hợp ngữ) và lưu vào một file .lts
