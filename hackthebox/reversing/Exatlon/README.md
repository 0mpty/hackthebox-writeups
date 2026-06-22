# Exatlon - Reverse Engineering Writeup

**Author:** Empty(0mpty) 
**Date:** 22.06.2026 
**Difficulty:** Easy 
**Category:** Reverse Engineering

**Tools:** UPX, Ghidra, GDB/edb, Python

## Description
Binary packed with UPX. After unpacking, it asks for password and validates using bit shifting encryption.

## Analysis
1. **Unpack UPX:** `upx -d exatlon`
2. **Ghidra:** Initial static analysis shows encrypted values but decompiler doesn't clearly reveal the encryption logic
3. **GDB Dynamic Analysis:** Setting breakpoints and analyzing registers reveals the key instruction `shl eax, 4` - each character is shifted left by 4 bits (multiplied by 16)
4. **Understanding the Data:** The string of numbers `1152 1344 1056 1968 1728 816 1648 784 1584 816 1728 1520 1840 1664 784 1632 1856 1520 1728 816 1632 1856 1520 784 1760 1840 1824 816 1584 1856 784 1776 1760 528 528 2000` contains encrypted characters where each number represents one ASCII character multiplied by 16

## Decryption Script
The encryption algorithm is implemented in `exatlon_v1_script.py`
