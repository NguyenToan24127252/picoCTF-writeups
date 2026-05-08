### Bài toán
- Description
    - Using tabcomplete in the Terminal will add years to your life, esp. when dealing with long rambling directory structures and filename. Addadshashanammu.zip

### Giải
- Chỉ là mở file .c rồi lấy cờ thôi!
### Note
- Tính năng Tab-completion trong Bash không chỉ là một tiện ích, nó hoạt động dựa trên cơ chế:
    - Path Expansion: Bash sẽ quét thư mục hiện tại hoặc các thư mục trong biến môi trường $PATH để tìm các chuỗi ký tự khớp với những gì bạn đã gõ.
    - Context Awareness: Terminal hiện đại có khả năng hiểu ngữ cảnh. Nếu bạn gõ lệnh cd, phím Tab sẽ chỉ gợi ý các thư mục. Nếu bạn gõ python3, nó sẽ gợi ý các file có đuôi .py.
