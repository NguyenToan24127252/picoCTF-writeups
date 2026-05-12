### Bài toán
- Description
    - What does asm1(0x2ff) return? Submit the flag as a hexadecimal value (starting with '0x'). NOTE: Your submission for this question will NOT be in the normal flag format. Source

### Giải
- Code:
```
asm1:
        <+0>:   endbr32 
        <+4>:   push   ebp
        <+5>:   mov    ebp,esp
        <+7>:   cmp    DWORD PTR [ebp+0x8],0x753
        <+14>:  jg     0x11d6 <asm1+41>
        <+16>:  cmp    DWORD PTR [ebp+0x8],0x5af
        <+23>:  jne    0x11ce <asm1+33>
        <+25>:  mov    eax,DWORD PTR [ebp+0x8]
        <+28>:  add    eax,0x7
        <+31>:  jmp    0x11ed <asm1+64>
        <+33>:  mov    eax,DWORD PTR [ebp+0x8]
        <+36>:  sub    eax,0x7
        <+39>:  jmp    0x11ed <asm1+64>
        <+41>:  cmp    DWORD PTR [ebp+0x8],0x907
        <+48>:  jne    0x11e7 <asm1+58>
        <+50>:  mov    eax,DWORD PTR [ebp+0x8]
        <+53>:  sub    eax,0x7
        <+56>:  jmp    0x11ed <asm1+64>
        <+58>:  mov    eax,DWORD PTR [ebp+0x8]
        <+61>:  add    eax,0x7
        <+64>:  pop    ebp
        <+65>:  ret    
```
- Trong x86 32-bit, tham số đầu tiên truyền vào hàm nằm ở vị trí [ebp+0x8] => [ebp+0x8] = 0x2ff
- So sánh lần 1 ở <+7>, <+14>:
    - So sánh 0x2ff và 0x753 do 0x2ff < 0x753 nên không nhảy (jg - (Jump if Greater - Nhảy nếu lớn hơn))
    - Đi tiếp xuống <+16>
- So sánh lần 2 ở <+16> và <+23>:
    - So sánh 0x2ff với 0x5af do 0x2ff != 0x5af điều kiện jne (Jump if Not Equal - Nhảy nếu không bằng) thỏa mãn.
    - Nhảy tới <+33>
- Thực hiện phép toán tại <+33>
    - Đưa giá trị 0x2ff vào thanh ghi eax.
    - Thực hiện: eax = eax - 0x7.
    - Tính toán: 0x2ff - 0x7 = 0x2f8.
    - Kết quả: Nhảy tới <+64> để kết thúc hàm.
