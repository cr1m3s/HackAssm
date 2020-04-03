#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
filename = sys.argv[1]
file_format = filename.split(".")[1]
if file_format != "asm":
    print("Wrong file format!")
    sys.exit()

compute = {'0': '0101010', '1': '0111111', '-1': '0111010',
           'D': '0001100', 'A': '0110000', '!D': '0001101',
           '!A': '0110001', '-D': '0001111', '-A': '0110011',
           'D+1': '0011111', 'A+1': '0110111', 'D-1': '0001110',
           'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011',
           'A-D': '0000111', 'D&A': '0000000', 'D|A': '0010101',
           'M': '1110000', '!M': '1110001', '-M': '1110011',
           'M+1': '1110111', 'M-1': '1110010', 'D+M': '1000010',
           'D-M': '1010011', 'M-D': '1000111', 'D&M': '1000000',
           'D|M': '1010101'}

dest = {'null': '000', 'M': '001', 'D': '010', 'MD': '011',
        'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'}

jump = {'null': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
        'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}

predef_symbols = {'SCREEN': 16384, 'KBD': 24576, 'SP': 0, 'LCL': 1,
                  'ARG': 2, 'THIS': 3, 'THAT': 4}

result = ''
content = []

with open(filename) as f:
    content = f.read()
all_lines = content.split("\n")
non_empty_lines = [line for line in all_lines if line.strip() != ""]
f.close()


def binary_repr(num):
    result = ''
    number = int(num)
    while number > 0:
        result += str(number % 2)
        number = number // 2
    result += (16-len(result))*'0'
    return result[::-1]


def symbol_code(symbol):
    if symbol[0] == 'R':
        number = symbol[1::]
        if int(number) > 15:
            print("HAL supports only R0..R15, not a  R{0}".format(number))
            sys.exit()
        return binary_repr(number)
    elif symbol in predef_symbols:
        return binary_repr(predef_symbols[symbol])
    else:
        return binary_repr(symbol)


def op_code(instr):
    op_set = instr.split("=")
    result = '111' + compute[op_set[1]] + dest[op_set[0]] + jump['null']
    return result


def read_labels(lines):
    result = {}
    inst_counter = 1
    for sub_line in lines:
        if sub_line[0] == '(':
            result.update({sub_line[1:-1]: binary_repr(inst_counter)})
        inst_counter += 1
    return result


result = ''
label_symbols = read_labels(non_empty_lines)
for line in non_empty_lines:
    line = line.strip()
    if line[0] not in '(/':
        if line[0] == "@":
            symbol = line[1::]
            if symbol in label_symbols:
                result += str(label_symbols[symbol])
            else:
                result += str(symbol_code(symbol))
        else:
            result += op_code(line)
        result += '\n'
print(result)
hack_filename = filename.split('.')[0] + '.hack'
hack_file = open(hack_filename, "w")
hack_file.write(result)
hack_file.close()
