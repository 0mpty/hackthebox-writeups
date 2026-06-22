code = [1152, 1344, 1056, 1968, 1728, 816, 1648, 784, 1584, 816, 1728, 1520, 1840, 1664, 784, 1632, 1856, 1520, 1728, 816, 1632, 1856, 1520, 784, 1760, 1840, 1824, 816, 1584, 1856, 784, 1776, 1760, 528, 528, 2000]

def decode(code):
    for val in code:
        hex_val = int(hex(val), 16)
        encrypt_code = hex_val >> 4
        print(chr(encrypt_code), end="")

decode(code)
