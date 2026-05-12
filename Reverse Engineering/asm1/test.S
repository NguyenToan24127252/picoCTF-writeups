asm1:
	<+0>:	endbr32 
	<+4>:	push   ebp
	<+5>:	mov    ebp,esp
	<+7>:	cmp    DWORD PTR [ebp+0x8],0x753
	<+14>:	jg     0x11d6 <asm1+41>
	<+16>:	cmp    DWORD PTR [ebp+0x8],0x5af
	<+23>:	jne    0x11ce <asm1+33>
	<+25>:	mov    eax,DWORD PTR [ebp+0x8]
	<+28>:	add    eax,0x7
	<+31>:	jmp    0x11ed <asm1+64>
	<+33>:	mov    eax,DWORD PTR [ebp+0x8]
	<+36>:	sub    eax,0x7
	<+39>:	jmp    0x11ed <asm1+64>
	<+41>:	cmp    DWORD PTR [ebp+0x8],0x907
	<+48>:	jne    0x11e7 <asm1+58>
	<+50>:	mov    eax,DWORD PTR [ebp+0x8]
	<+53>:	sub    eax,0x7
	<+56>:	jmp    0x11ed <asm1+64>
	<+58>:	mov    eax,DWORD PTR [ebp+0x8]
	<+61>:	add    eax,0x7
	<+64>:	pop    ebp
	<+65>:	ret    

