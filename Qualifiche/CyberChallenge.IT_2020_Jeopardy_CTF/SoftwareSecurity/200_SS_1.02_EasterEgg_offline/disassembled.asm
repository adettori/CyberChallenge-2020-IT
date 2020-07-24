push   rbp
4008f3  mov    rbp,rsp
4008f6  sub    rsp,0x60
4008fa  mov    QWORD PTR [rbp-0x58],rdi
4008fe  mov    rax,QWORD PTR fs:0x28
400907  mov    QWORD PTR [rbp-0x8],rax
40090b  xor    eax,eax
40090d  mov    edi,0x1
400912  call   0x400660 <sleep@plt>
400917  mov    rax,QWORD PTR [rbp-0x58]
40091b  mov    rdi,rax
40091e  call   0x4005f0 <strlen@plt>
400923  cmp    rax,0xa
400927  jne    0x4009c3 <check_password+209>
40092d  mov    rax,QWORD PTR [rbp-0x58]
400931  movzx  eax,BYTE PTR [rax]
400934  cmp    al,0x57
400936  jne    0x4009c3 <check_password+209>
40093c  mov    rax,QWORD PTR [rbp-0x58]
400940  add    rax,0x1
400944  movzx  eax,BYTE PTR [rax]
400947  cmp    al,0x41
400949  jne    0x4009c3 <check_password+209>
40094b  mov    rax,QWORD PTR [rbp-0x58]
40094f  add    rax,0x2
400953  movzx  eax,BYTE PTR [rax]
400956	cmp    al,0x49
400958	jne    0x4009c3 <check_password+209>
40095a	mov    rax,QWORD PTR [rbp-0x58]
40095e	add    rax,0x3
400962	movzx  eax,BYTE PTR [rax]
400965	cmp    al,0x54
400967	jne    0x4009c3 <check_password+209>
400969	mov    rax,QWORD PTR [rbp-0x58]
40096d	add    rax,0x4
400971	movzx  eax,BYTE PTR [rax]
400974	cmp    al,0x36
400976	jne    0x4009c3 <check_password+209>
400978	mov    rax,QWORD PTR [rbp-0x58]
40097c	add    rax,0x5
400980	movzx  eax,BYTE PTR [rax]
400983	cmp    al,0x35
400985	jne    0x4009c3 <check_password+209>
400987	mov    rax,QWORD PTR [rbp-0x58]
40098b	add    rax,0x6
40098f	movzx  eax,BYTE PTR [rax]
400992	cmp    al,0x30
400994	jne    0x4009c3 <check_password+209>
400996	mov    rax,QWORD PTR [rbp-0x58]
40099a	add    rax,0x7
40099e	movzx  eax,BYTE PTR [rax]
4009a1	cmp    al,0x32
4009a3	jne    0x4009c3 <check_password+209>
4009a5	mov    rax,QWORD PTR [rbp-0x58]
4009a9	add    rax,0x8
4009ad	movzx  eax,BYTE PTR [rax]
4009b0	cmp    al,0x2c
4009b2	jne    0x4009c3 <check_password+209>
4009b4	mov    rax,QWORD PTR [rbp-0x58]
4009b8	add    rax,0x9
4009bc	movzx  eax,BYTE PTR [rax]
4009bf	cmp    al,0x31
4009c1	je     0x4009cd <check_password+219>
4009c3	mov    eax,0x1
4009c8	jmp    0x400a54 <check_password+354>
4009cd	movabs rax,0x202c646565646e49
4009d7	movabs rdx,0x6568742064616572
4009e1	mov    QWORD PTR [rbp-0x50],rax
4009e5	mov    QWORD PTR [rbp-0x48],rdx
4009e9	movabs rax,0x7473206c6c756620
4009f3	movabs rdx,0x657265682079726f
4009fd	mov    QWORD PTR [rbp-0x40],rax
400a01	mov    QWORD PTR [rbp-0x38],rdx
400a05	movabs rax,0x3a7370747468203a
400a0f	movabs rdx,0x61702e7777772f2f
400a19	mov    QWORD PTR [rbp-0x30],rax
400a1d	mov    QWORD PTR [rbp-0x28],rdx
400a21	movabs rax,0x2e656c6261746567
400a2b	movabs rdx,0x343d703f2f6d6f63
400a35	mov    QWORD PTR [rbp-0x20],rax
400a39	mov    QWORD PTR [rbp-0x18],rdx
400a3d	mov    WORD PTR [rbp-0x10],0x33
400a43	lea    rax,[rbp-0x50]
400a47	mov    rdi,rax
400a4a	call   0x4005e0 <puts@plt>
400a4f	mov    eax,0x0
400a54	mov    rcx,QWORD PTR [rbp-0x8]
400a58	xor    rcx,QWORD PTR fs:0x28
400a61	je     0x400a68 <check_password+374>
400a63	call   0x400600 <__stack_chk_fail@plt>
400a68	leave
400a69	ret
