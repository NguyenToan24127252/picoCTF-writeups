### Bài toán
- Description
    - Cryptography can be easy, do you know what ROT13 is?
        values.txt

### Giải
- Vì bài này dùng ROT13, mỗi chữ cái được dịch đi 13 vị trí. Chúng ta sẽ dùng lệnh tr (translate) để dịch ngược lại: 
```
cat values.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```
- Với:
    - A-Z trở thành N-ZA-M: Chữ A (vị trí 1) dịch 13 thành N (vị trí 14), và cứ thế xoay vòng.
    - a-z trở thành n-za-m: Tương tự cho chữ thường.
### Note
- ROT13 (viết tắt của "rotate by 13 places"). Đây là một dạng đặc biệt của mật mã Caesar:
    - Bảng chữ cái tiếng Anh có 26 chữ cái.
    - ROT13 sẽ dịch chuyển mỗi chữ cái đi 13 vị trí.
    - Vì 13=26/2, nên nếu bạn thực hiện ROT13 hai lần trên cùng một văn bản, bạn sẽ nhận lại văn bản gốc ban đầu (13+13=26 = 0 (mod 26))
