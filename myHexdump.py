#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

def cut(str):
    ''' Cut a string after the 16th character '''
    line = ''
    if (len(str) < 16):
        return (str, '')
    else:
        i = len(str) - 16
        line = str[:16]
        end = str[16:]
        return (line, end)

def fmt_hex(str):
    ''' Convert a string in hexadecimal '''
    out = []
    for c in str:
        out.append(c.encode('hex'))
    return out

def fmt_asciirepr(str):
    ''' Convert a string in ascii '''
    out = []
    for c in str:
        if 32 <= ord(c) <= 126:
            out.append(c)
        else:
            out.append('.')
    return out

def fmt_line(num, str):
    ''' Hexdump output format '''
    if str == '':
        print '%08x' % num
        return
    hex = ''
    for c in fmt_hex(str):
        if len(hex) == 24:
            hex += ' '
        hex += ' ' + c
    ascii = ''
    for c in fmt_asciirepr(str):
        ascii += c

    length = len(str)
    if length < 16:
        pos = 49 - len(hex)
        print '%08x %s %s |%s|' % (num, hex, ' ' * pos, ascii)
    else:
        print '%08x %s  |%s|' % (num, hex, ascii)

def hexdump(file):
    ''' Just like hexdump -C <file> '''
    try:
        fd = open(file)
    except:
        print 'error : unable to open %s' % (file)

    lines = fd.readlines()
    buf = ''
    num = 0
    for line in lines:
        buf += line
        (start, end) = cut(buf)
        if len(start) == 16:
            fmt_line(num, start)
            num += 16
            buf = end
        else:
            buf = start

    buf = end
    while buf != '':
        (start, end2) = cut(buf)
        if len(start) == 16:
            fmt_line(num, start)
            num += 16 
            buf = end2
        else:
            fmt_line(num, start)
            buf = ''
            num += len(start)
    fmt_line(num, '')
    fd.close()

if __name__ == '__main__':
    ''' Main function '''
    try:
        hexdump(sys.argv[1])
    except:
        print 'usage : %s <file>' % (sys.argv[0])

