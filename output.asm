BITS 64
%define SYS_EXIT 60
segment .text
global _start
put:
        push    rbp
        mov     rbp, rsp
        sub     rsp, 64
        mov     QWORD [rbp-56], rdi
        mov     DWORD [rbp-4], 1
        mov     eax, DWORD [rbp-4]
        cdqe
        mov     edx, 32
        sub     rdx, rax
        mov     BYTE [rbp-48+rdx], 10
.L2:
        mov     rcx, QWORD [rbp-56]
        mov     rdx, 7378697629483820647
        mov     rax, rcx
        imul    rdx
        sar     rdx, 2
        mov     rax, rcx
        sar     rax, 63
        sub     rdx, rax
        mov     rax, rdx
        sal     rax, 2
        add     rax, rdx
        add     rax, rax
        sub     rcx, rax
        mov     rdx, rcx
        mov     eax, edx
        lea     ecx, [rax+48]
        mov     eax, DWORD [rbp-4]
        lea     edx, [rax+1]
        mov     DWORD [rbp-4], edx
        cdqe
        mov     edx, 31
        sub     rdx, rax
        mov     eax, ecx
        mov     BYTE [rbp-48+rdx], al
        mov     rcx, QWORD [rbp-56]
        mov     rdx, 7378697629483820647
        mov     rax, rcx
        imul    rdx
        mov     rax, rdx
        sar     rax, 2
        sar     rcx, 63
        mov     rdx, rcx
        sub     rax, rdx
        mov     QWORD [rbp-56], rax
        cmp     QWORD [rbp-56], 0
        jg      .L2
        mov     eax, DWORD [rbp-4]
        cdqe
        mov     edx, DWORD [rbp-4]
        movsx   rdx, edx
        mov     ecx, 32
        sub     rcx, rdx
        lea     rdx, [rbp-48]
        add     rcx, rdx
        mov     rdx, rax
        mov     rsi, rcx
        mov     edi, 1
        mov     rax, 1
        syscall
        nop
        leave
        ret
main:
        push    rbp
        mov     rbp, rsp
        sub     rsp, 16
        ;; -- assign foo -- 
         mov     QWORD [rbp - 8], 34
        ;; -- assign bar -- 
         mov     QWORD [rbp - 16], 35
        ;;-- plus --
        mov     rax, QWORD [rbp - 8]
        mov     rbx, QWORD [rbp - 16]
        add     rax, rbx
        ;; -- assign foo -- 
         mov     QWORD [rbp - 24], rax
        ;; -- put --
        mov rdi, QWORD [rbp - 24]
        call put
        ;; -- assign foo -- 
         mov     QWORD [rbp - 32], 500
        ;; -- assign bar -- 
         mov     QWORD [rbp - 40], 80
        ;;-- minus --
        mov     rax, QWORD [rbp - 32]
        mov     rbx, QWORD [rbp - 40]
        sub     rax, rbx
        ;; -- assign baz -- 
         mov     QWORD [rbp - 48], rax
        ;; -- put --
        mov rdi, QWORD [rbp - 48]
        call put
        mov rax, SYS_EXIT
        mov rdi, 1
        syscall
_start:
        call main
