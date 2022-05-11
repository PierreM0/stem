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


OP_ASSIGN = iota(True)
OP_PLUS   = iota()
OP_MINUS  = iota()
OP_PUT    = iota()
OP_EQUAL  = iota()
# OP_WHILE  = iota()
# OP_OPEN_BRACKET  = iota()
# OP_CLOSE_BRACKET = iota()

OP_SEMICOLON = iota()
COUNT_OPS = iota()

VAR = iota()
INT = iota()


### OPERATIONS #####
def assign(x, y):
    return (OP_ASSIGN, x, y)

def plus(x, y):
    return (OP_PLUS, x, y)

def minus(x, y):
    return (OP_MINUS, x, y)

def equal(x, y):
    return(OP_EQUAL, x, y)

def put(x):
    return(OP_PUT, x)


lexer_line = 0
lexer_col  = 0

def left_strip(string):
    col = 0
    line = 0
    while (col+line) < len(string) and string[col+line].isspace():
        if string[col+line] == '\n':
            line, col = line + 1 , 0
        else:
            col += 1
    return (col, line, string[col+line:])
        
class Lexer:

    def __init__(self, src, file_path):
        self.src = src
        self.file_path = file_path
    
    def next(self):
        global lexer_line
        global lexer_col

        assert COUNT_OPS == 6, "Op count changed in Lexer().next()"
        
        scol, sline, self.src = left_strip(self.src)
        lexer_line += sline
        if sline > 0:
            lexer_col  = scol
        else:
            lexer_col += scol
        
        pos = (self.file_path, lexer_line, lexer_col)
        
        if len(self.src) == 0:
            return None
        
        if self.src[0] == '+':
            self.src = self.src[1:]
            lexer_col += 1
            return (OP_PLUS, '+', pos)
        elif self.src[0] == '-':
            self.src = self.src[1:]
            lexer_col += 1
            return (OP_MINUS, '-', pos)
        elif self.src[0] == '=':
            self.src = self.src[1:]
            lexer_col += 1
            return (OP_EQUAL, '=', pos)
        elif self.src[0] == ';':
            self.src = self.src[1:]
            lexer_col += 1
            return (OP_SEMICOLON, ';', pos)
        elif self.src[0] == ':':
            if self.src[1] == '=':
                self.src = self.src[2:]
                lexer_col += 2
                return (OP_ASSIGN, ':=', pos)
            else:
                print(f"\"{self.file_path}\":{lexer_line}:{lexer_col}: ERROR: `{self.src[0]}` is not a reconizable token")
                exit(1)
        elif self.src[0].isalpha():
            token = ""
            i = 0
            while i < len(self.src) and self.src[i].isalnum():
                token += self.src[i] 
                i += 1
            self.src = self.src[len(token):]
            lexer_col += i
            if token == "put":
                return (OP_PUT, token, pos)
            else:
                return (VAR, token, pos)
        elif self.src[0].isnumeric():
            token = ""
            i = 0
            while i < len(self.src) and self.src[i].isnumeric():
                token += self.src[i]
                i += 1
            self.src = self.src[len(token):]
            lexer_col += i
            return (INT, int(token), pos)
        elif self.src[0] == '\n':
            lexer_col = 0
            lexer_line += 1
        elif self.src[0].isspace() and self.src[0] != '\n':
            self.src = self.src[1:]
            lexer_col += 1
        else:
            print(f"\"{self.file_path}\":{lexer_line}:{lexer_col}: ERROR: `{self.src[0]}` is not a reconizable token")
            exit(1)
        


def parse_primary(lexer):
    token = lexer.next()
    if token != None:
        return token
    else:
        assert False, "unreachable"
    
    
def parse(lexer):
    lvalue = parse_primary(lexer)
    
    assert COUNT_OPS == 6, "Op count changed in parse()"

    if lvalue[0] == OP_PUT:
        rvalue = parse(lexer)
        return put(rvalue)
    elif lvalue[0] == OP_SEMICOLON:
        return None
    else:
        op_token = lexer.next()
        if op_token != None:
            if op_token[0] == OP_PLUS:
                rvalue = parse(lexer)
                return plus(lvalue, rvalue)
            elif op_token[0] == OP_MINUS:
                rvalue = parse(lexer)
                return minus(lvalue, rvalue)
            elif op_token[0] == OP_ASSIGN:
                rvalue = parse(lexer)
                return assign(lvalue, rvalue)
            elif op_token[0] == OP_EQUAL:
                rvalue = parse(lexer)
                return equal(lvalue, rvalue)
            else:
                f, l, c = op_token[2]
                print(f"\"{f}\":{l}:{c} ERROR: unexpected binary operation `{op_token[1]}`")
                exit(1)
    return lvalue
        
def load_program_from_file(prog_path):
    f  = open(prog_path, "r")
    program = [parse(Lexer(string, prog_path)) for string in f.read().split(';')]
    return program
    
var_dict = {}
#### SIMULATE AND COMPILE PROGRAM #####
def simulate_program(program):
    """Simulate the program."""
    global var_dict
    
    assert COUNT_OPS == 6, "Op count changed in simulate_program()"
    for op in program:
        if op[0] == OP_ASSIGN:
            tmp = op[2][1]
            if type(op[2][1]) == tuple:
                tmp = [op[2]]
                tmp = simulate_program(tmp)
            var_dict[op[1][1]] = tmp
        elif op[0] == OP_PLUS:
            if type(op[1][1]) == str:
                var1 = var_dict[op[1][1]]
            else:
                var1 = op[1][1]
            if type(op[2][1]) == str:
                var2 = var_dict[op[2][1]]
            else:
                var2 = op[2][1]
            return var1 + var2
            
        elif op[0] == OP_MINUS:
            if type(op[1][1]) == str:
                var1 = var_dict[op[1][1]]
            else:
                var1 = op[1][1]
            if type(op[2][1]) == str:
                var2 = var_dict[op[2][1]]
            else:
                var2 = op[2][1]
            return var1 - var2
        elif op[0] == OP_EQUAL:
            if type(op[1][1]) == str:
                var1 = var_dict[op[1][1]]
            else:
                var1 = op[1][1]
            if type(op[2][1]) == str:
                var2 = var_dict[op[2][1]]
            else:
                var2 = op[2][1]
            res = 1 if var1 == var2 else 0
            return res
        elif op[0] == OP_PUT:
            if type(op[1][1]) == str:
                var = var_dict[op[1][1]]
            else:
                var = op[1][1]
            print(var)
        else:
            print(op)
            assert False, "unreachable"

esp_add = 0
def compile_program(file_name, program):
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
    
        assert COUNT_OPS == 6, "Op count changed in compile_program()"
        for op in program:
            if op[0] == OP_ASSIGN:
                tmp = op[2][1]
                if type(op[2][1]) == tuple:
                    tmp = [op[2]]
                    string = compile_program(file_name, tmp)
                    f.write(string)
                    tmp = "rax"
                esp_add += 8
                var_dict[op[1][1]] = esp_add 
                f.write( "        ;; -- assign %s -- \n" % op[1][1])
                f.write( " ")
                f.write(f"        mov     QWORD [rbp - {esp_add}], {tmp}\n")
                    
            elif op[0] == OP_PLUS:
                if type(op[1][1]) == str:
                    var1 = "QWORD [rbp - " + str(var_dict[op[1][1]]) + "]"
                else:
                    var1 = str(op[1][1])
                if type(op[2][1]) == str:
                    var2 = "QWORD [rbp - " + str(var_dict[op[2][1]])+ "]"
                else:
                    var2 = str(op[2][1])
                string  = "        ;;-- plus --\n"
                string += "        mov     rax, %s\n" % var1
                string += "        mov     rbx, %s\n" % var2
                string += "        add     rax, rbx\n"
                return string
            
            elif op[0] == OP_MINUS:
                if type(op[1][1]) == str:
                    var1 = "QWORD [rbp - " + str(var_dict[op[1][1]]) + "]"
                else:
                    var1 = str(op[1][1])
                if type(op[2][1]) == str:
                    var2 = "QWORD [rbp - " + str(var_dict[op[2][1]])+ "]"
                else:
                    var2 = str(op[2][1])
                string  = "        ;;-- minus --\n"
                string += "        mov     rax, %s\n" % var1
                string += "        mov     rbx, %s\n" % var2
                string += "        sub     rax, rbx\n"
                return string

            elif op[0] == OP_EQUAL:
                if type(op[1][1]) == str:
                    var1 = "QWORD [rbp - " + str(var_dict[op[1][1]]) + "]"
                else:
                    var1 = str(op[1][1])
                if type(op[2][1]) == str:
                    var2 = "QWORD [rbp - " + str(var_dict[op[2][1]])+ "]"
                else:
                    var2 = str(op[2][1])
                string  = "        ;;-- equal --\n"
                string += "        mov     rax, %s\n" % var1
                string += "        cmp     rax, %s\n" % var2
                string += "        sete    al      \n"
                string += "        movzx   rax, al\n"
                return string
            
            elif op[0] == OP_PUT:
                if type(op[1][1]) == str:
                    var = "QWORD [rbp - " + str(var_dict[op[1][1]]) + "]"
                else:
                    var = str(op[1][1])
                f.write("        ;; -- put --\n")
                f.write("        mov rdi, %s\n" % var)
                f.write("        call put\n")
            else:
                print(op)
                assert False, "unreachable"

        f.write("        mov rax, SYS_EXIT\n")
        f.write("        mov rdi, 1\n")
        f.write("        syscall\n")
        f.write("_start:\n")
        f.write("        call main\n")
        f.close()

def usage():
    print("ERROR: usage ./stem.py [SUBCOMMAND] <program>")
    print("SUBCOMMANDS:")
    print("    com: compile the program")
    print("    sim: simulate the program")

def shift(lst):
    return (lst[0], lst[1:])

def main():

    argv = sys.argv
    
    assert len(argv) > 1
    prg_name, argv = shift(argv)
    if len(argv) < 1:
        usage()
        exit(1)
        
    subcommand, argv = shift(argv)
    prg_path,   argv = shift(argv)
    
    program = load_program_from_file(prg_path)

    if subcommand == "sim":
        simulate_program(program)
        
    elif subcommand == "com":
        compile_program("output.asm", program)
        run_and_write(["nasm", "-felf64", "output.asm"])
        run_and_write(["ld", "-o", "output", "output.o"])

    else:
        print(f"ERROR: unknown subcommand {subcommand}")
        exit(1)

    
if __name__ == '__main__':
    main()
