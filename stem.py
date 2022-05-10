#! /usr/bin/python
import sys
import subprocess


def run_and_write(lst):
    for el in lst:
        print(el, end=" ")
    print()
    subprocess.run(lst)
    
iota__ = -1

def iota(reset = False):
    global iota__
    iota__ += 1
    if reset:
        iota__ = 0
    return iota__


OP_ASSIGN = iota()
OP_PLUS   = iota()
OP_MINUS  = iota()
OP_PUT    = iota()
COUNT_OPS = iota()

### OPERATIONS #####
def assign(x, y):
    return (OP_ASSIGN, x, y)

def plus(x, y):
    return (OP_PLUS, x, y)

def minus(x, y):
    return (OP_MINUS, x, y)

def put(x):
    return(OP_PUT, x)


var_dict = {}
#### SIMULATE AND COMPILE PROGRAM #####
def simulate_program(program):
    """Simulate the program."""
    global var_dict
    
    assert COUNT_OPS == 4, "Op count changed in simulate_program()"
    for op in program:
        if op[0] == OP_ASSIGN:
            if type(op[2]) == tuple:
                tmp = [op[2]]
                var_dict[op[1]] = simulate_program(tmp)
            else:
                var_dict[op[1]] = op[2]
                
        elif op[0] == OP_PLUS:
            if type(op[1]) == str:
                tmp = var_dict[op[1]] + var_dict[op[2]]
            else:
                tmp = op[1] + op[2] 
            return tmp
        
        elif op[0] == OP_MINUS:            
            if type(op[1]) == str:
                tmp = var_dict[op[1]] - var_dict[op[2]]
            else:
                tmp = op[1] - op[2] 
            return tmp
        
        elif op[0] == OP_PUT:
            if type(op[1]) == str:
                print(var_dict[op[1]])
            else:
                print(op[1])      
        else:
            assert False, "unreatchable "
            
esp_add = 0
def compile_program(file_name, program, rec = False):
    """Open a file and write assembly code in it."""
    global esp_add
    global var_dict

    with open("output.asm", "w") as f:
        f.write("BITS 64\n")
        f.write("%define SYS_EXIT 60\n")
        f.write("segment .text\n")
        f.write("global _start\n")
        f.write("put:\n")
        f.write("        push    rbp\n")
        f.write("        mov     rbp, rsp\n")
        f.write("        sub     rsp, 64\n")
        f.write("        mov     QWORD [rbp-56], rdi\n")
        f.write("        mov     DWORD [rbp-4], 1\n")
        f.write("        mov     eax, DWORD [rbp-4]\n")
        f.write("        cdqe\n")
        f.write("        mov     edx, 32\n")
        f.write("        sub     rdx, rax\n")
        f.write("        mov     BYTE [rbp-48+rdx], 10\n")
        f.write(".L2:\n")
        f.write("        mov     rcx, QWORD [rbp-56]\n")
        f.write("        mov     rdx, 7378697629483820647\n")
        f.write("        mov     rax, rcx\n")
        f.write("        imul    rdx\n")
        f.write("        sar     rdx, 2\n")
        f.write("        mov     rax, rcx\n")
        f.write("        sar     rax, 63\n")
        f.write("        sub     rdx, rax\n")
        f.write("        mov     rax, rdx\n")
        f.write("        sal     rax, 2\n")
        f.write("        add     rax, rdx\n")
        f.write("        add     rax, rax\n")
        f.write("        sub     rcx, rax\n")
        f.write("        mov     rdx, rcx\n")
        f.write("        mov     eax, edx\n")
        f.write("        lea     ecx, [rax+48]\n")
        f.write("        mov     eax, DWORD [rbp-4]\n")
        f.write("        lea     edx, [rax+1]\n")
        f.write("        mov     DWORD [rbp-4], edx\n")
        f.write("        cdqe\n")
        f.write("        mov     edx, 31\n")
        f.write("        sub     rdx, rax\n")
        f.write("        mov     eax, ecx\n")
        f.write("        mov     BYTE [rbp-48+rdx], al\n")
        f.write("        mov     rcx, QWORD [rbp-56]\n")
        f.write("        mov     rdx, 7378697629483820647\n")
        f.write("        mov     rax, rcx\n")
        f.write("        imul    rdx\n")
        f.write("        mov     rax, rdx\n")
        f.write("        sar     rax, 2\n")
        f.write("        sar     rcx, 63\n")
        f.write("        mov     rdx, rcx\n")
        f.write("        sub     rax, rdx\n")
        f.write("        mov     QWORD [rbp-56], rax\n")
        f.write("        cmp     QWORD [rbp-56], 0\n")
        f.write("        jg      .L2\n")
        f.write("        mov     eax, DWORD [rbp-4]\n")
        f.write("        cdqe\n")
        f.write("        mov     edx, DWORD [rbp-4]\n")
        f.write("        movsx   rdx, edx\n")
        f.write("        mov     ecx, 32\n")
        f.write("        sub     rcx, rdx\n")
        f.write("        lea     rdx, [rbp-48]\n")
        f.write("        add     rcx, rdx\n")
        f.write("        mov     rdx, rax\n")
        f.write("        mov     rsi, rcx\n")
        f.write("        mov     edi, 1\n")
        f.write("        mov     rax, 1\n")
        f.write("        syscall\n")
        f.write("        nop\n")
        f.write("        leave\n")
        f.write("        ret\n")
        f.write("main:\n")
        f.write("        push    rbp\n")
        f.write("        mov     rbp, rsp\n")
        f.write("        sub     rsp, 16\n")
    
        assert COUNT_OPS == 4, "Op count changed in compile_program()"
        for op in program:
            if op[0] == OP_ASSIGN:
                tmp = op[2]
                if type(op[2]) == tuple:
                    tmp = [op[2]]
                    string = compile_program(file_name, tmp, True)
                    f.write(string)
                    tmp = "rax"
                esp_add += 8
                var_dict[op[1]] = esp_add 
                f.write( "        ;; -- assign %s -- \n" % op[1])
                f.write( " ")
                f.write(f"        mov     QWORD [rbp - {esp_add}], {tmp}\n")
                    
            elif op[0] == OP_PLUS:
                if type(op[1]) == str:
                    var1 = "QWORD [rbp - " + str(var_dict[op[1]]) + "]"
                else:
                    var1 = str(op[1])
                if type(op[2]) == str:
                    var2 = "QWORD [rbp - " + str(var_dict[op[2]])+ "]"
                else:
                    var2 = str(op[2])
                string  = "        ;;-- plus --\n"
                string += "        mov     rax, %s\n" % var1
                string += "        mov     rbx, %s\n" % var2
                string += "        add     rax, rbx\n"
                return string
            
            elif op[0] == OP_MINUS:
                if type(op[1]) == str:
                    var1 = "QWORD [rbp - " + str(var_dict[op[1]]) + "]"
                else:
                    var1 = str(op[1])
                if type(op[2]) == str:
                    var2 = "QWORD [rbp - " + str(var_dict[op[2]])+ "]"
                else:
                    var2 = str(op[2])
                string  = "        ;;-- minus --\n"
                string += "        mov     rax, %s\n" % var1
                string += "        mov     rbx, %s\n" % var2
                string += "        sub     rax, rbx\n"
                return string

            elif op[0] == OP_PUT:
                if type(op[1]) == str:
                    var = "QWORD [rbp - " + str(var_dict[op[1]]) + "]"
                else:
                    var = str(op[1])
                f.write("        ;; -- put --\n")
                f.write("        mov rdi, %s\n" % var)
                f.write("        call put\n")
            else:
                assert False, "unreachable"

        f.write("        mov rax, SYS_EXIT\n")
        f.write("        mov rdi, 1\n")
        f.write("        syscall\n")

        f.write("_start:\n")
        f.write("        call main\n")
        f.close()
                
def main():

    program = [
        assign("foo", 34),
        assign("bar", 35),
        assign("foo", plus("foo", "bar")),
        put("foo"),
        assign("foo", 500),
        assign("bar", 80),
        assign("baz", minus("foo", "bar")),
        put("baz")
    ]

    if len(sys.argv) < 2:
        print("ERROR: usage ./stem.py [SUBCOMMAND] <program>")
        print("SUBCOMMANDS:")
        print("    com: compile the program")
        print("    sim: simulate the program")
        exit(1)
        
    subcommand = sys.argv[1]

    if subcommand == "sim":

        simulate_program(program)
    elif subcommand == "com":
        compile_program("output.asm", program)
        run_and_write(["nasm", "-felf64", "output.asm"])
        run_and_write(["ld", "-o", "output", "output.o"])

    else:
        print(f"ERROR: unknown subcommand {subcommand}")


    
if __name__ == '__main__':
    main()
