asm2:
	<+0>:	endbr32 
	<+4>:	push   ebp
	<+5>:	mov    ebp,esp
	<+7>:	sub    esp,0x10
	<+10>:	mov    eax,DWORD PTR [ebp+0xc]
	<+13>:	mov    DWORD PTR [ebp-0x4],eax
	<+16>:	mov    eax,DWORD PTR [ebp+0x8]
	<+19>:	mov    DWORD PTR [ebp-0x8],eax
	<+22>:	jmp    0x11cd <asm2+32>
	<+24>:	add    DWORD PTR [ebp-0x4],0x1
	<+28>:	add    DWORD PTR [ebp-0x8],0x37
	<+32>:	cmp    DWORD PTR [ebp-0x8],0x84ab
	<+39>:	jle    0x11c5 <asm2+24>
	<+41>:	mov    eax,DWORD PTR [ebp-0x4]
	<+44>:	leave  
	<+45>:	ret    

