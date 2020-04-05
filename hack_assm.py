#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

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


def binary_repr(num):
    result = ''
    number = int(num)
    while number > 0:
        result += str(number % 2)
        number = number // 2
    result += (16-len(result))*'0'
    return result[::-1]

# possible instructions : a-, c-instructions
# simple solution for c-instructions, not works for jump instructions


def op_code(instr):
    op_set = instr.split("=")
    result = '111' + compute[op_set[1]] + dest[op_set[0]] + jump['null']
    return result


# a-instructions starts with 0[Nx15]
# a-instruction could be @number, @variable, @r[0..15],
# (LOOP)-depends from position where appears
# i.e. number of line for the next instruction
# @variable equals to 16+
# c-instructions starts with 111[a[cx6][dx3][jx3]]

def read_symbols(lines):
    result = {}
    counter = 0
    for line in lines:
        if line[0] == '(':
            result.update({line[1:-1]: counter})
        else:
            counter += 1
    return result


def comment_remove(line):
    line = line.split('/')[0].strip()
    return line


# check file format
filename = sys.argv[1]
file_format = filename.split(".")[1]
if file_format != "asm":
    print("Wrong file format!")
    sys.exit()

# read file content and remove whitespaces
content = []
with open(filename) as f:
    content = f.read()
all_lines = content.split("\n")
non_empty_lines = [line for line in all_lines
                   if line.strip() != "" and line[0] != '/']
f.close()

# parse lines and prepare string for output
result = ''
label_symbols = read_symbols(non_empty_lines)
variables = {}
mem_count = 16
for line in non_empty_lines:
    line = line.strip()
    if '/' in line:
        line = comment_remove(line)

    if line[0] == '@':
        # only a-instructions starts with @
        subline = line[1:]
        if subline in label_symbols:
            # replaced @JUMP instructions (XXX)
            result += binary_repr(label_symbols[subline])
        elif subline in predef_symbols:
            # parse predefine symbols
            result += binary_repr(predef_symbols[subline])
        elif subline.isnumeric():
            # parse simple numbers
            result += binary_repr(subline)
        elif subline in variables:
            # parse variables created by user
            result += binary_repr(variables[subline])
        elif subline[0] == 'R':
            # parse registers call
            if int(subline[1:]) <= 15:
                result += binary_repr(subline[1:])
            else:
                print("Register with number > 15 not allowed:  {0}"
                      .format(subline[1:]))
        else:
            # left only case when variable occures first time
            # add new variable to variables list
            # and to result
            # value depends on mem_address counter and starts with 16
            variables.update({subline: mem_count})
            mem_count += 1
            result += binary_repr(variables[subline])
        result += '\n'
    elif line[0] != '(':
        # parser for 2 tipes of c-instructions
        if ';' in line:
            # jump instructions
            subline = line.split(';')
            result += '111' + compute[subline[0]]\
                + dest['null'] + jump[subline[1]]
        elif '=' in line:
            # value assigment
            subline = line.split('=')
            result += '111' + compute[subline[1]]\
                + dest[subline[0]] + jump['null']
        result += '\n'

# write result into the .hack file with same name as .asm file
hack_filename = filename.split('.')[0] + '.hack'
hack_file = open(hack_filename, "w")
hack_file.write(result)
print("{0} translated\n{1} file created".format(filename, hack_filename))
hack_file.close()
