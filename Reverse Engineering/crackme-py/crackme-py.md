### Bài toán
- Description
    - just file crackme_gen.py

### Giải
- Sửa dòng cuối cùng của file từ choose_greatest() thành:
```
decode_secret(bezos_cc_secret)
```
### Note
- Bài toán cung cấp một file Python chứa hai hàm chính và một chuỗi đã mã hóa:
    - bezos_cc_secret: Chuỗi mục tiêu cần giải mã: "A:4@r%uL>0c0Abc?FE0g_47fgaagg6ffN".
    - alphabet: Bảng chữ cái tham chiếu gồm 94 ký tự ASCII có thể in được (từ ! đến ~).
    - decode_secret(secret): Hàm thực hiện thuật toán ROT47. Tuy nhiên, trong file gốc, hàm này không được gọi.
    - choose_greatest(): Hàm so sánh hai số nhập từ người dùng. Đây là hàm duy nhất được thực thi khi chạy file, đóng vai trò là "mồi nhử" (obfuscation) để làm chệch hướng người chơi.
- Lý thuyết về ROT47 - ROT47 là một biến thể của ROT13. Thay vì chỉ xoay vòng 26 chữ cái tiếng Anh, ROT47 xoay vòng toàn bộ bảng mã ASCII từ giá trị 33 (!) đến 126 (~).
    - Độ dài bảng chữ cái (Alphabet length): 94 ký tự.
    - Hằng số xoay (Rotation constant): 47.Tính chất: Vì 47 = 94 / 2, nên thuật toán này có tính đối xứng. Nghĩa là việc mã hóa một chuỗi hai lần với ROT47 sẽ trả về chính chuỗi ban đầu. Hàm decode_secret trong bài thực chất cũng chính là hàm encode.