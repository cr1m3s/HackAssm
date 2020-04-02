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


def op_code(instr):
    op_set = instr.split("=")
    result = '111' + compute[op_set[1]] + dest[op_set[0]] + jump['null']
    return result


for line in non_empty_lines:
    if line[0] != '/':
        if line[0] in "0@":
            result += binary_repr(line[1::])
        else:
            result += op_code(line)
        result += '\n'

print(result)
hack_filename = filename.split('.')[0] + '.hack'
hack_file = open(hack_filename, "w")
hack_file.write(result)
hack_file.close()
