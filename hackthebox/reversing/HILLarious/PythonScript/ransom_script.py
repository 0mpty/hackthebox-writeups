import math

param_1 = [0] * 8
param_2 = [0] * 4

name = 'secret.txt.enc'
    
with open(name, 'rb') as text:
    doc = text.read()[20:]
    size = len(doc) + 1 & 0xfffffffffffffffe
    time = 1775046501
    const = 0xcbf29ce484222325

    i = 8
    while True:
        u1 = time & 0xff
        time = time >> 8
        const = (const ^ u1) * 0x100000001b3
        i -= 1
        
        if i == 0:
            break

    const = const ^ 0xdeadbeefcafebabe

    i = 0
    while True:
        shift = (i * 8 & 0x3f)
        param_1[i] = (const >> shift) & 0xff
        
        i += 1

        if i == 8:
            break

    l2 = const * 0x5851f42d4c957f2d + 0x6c576fac43fd007c
    u4 = l2
    u1 = u4 * 0x4c957f2d + 0xf767814f
    u3 = u1 & 0xff
    u4 = u4 & 0xff | 1
    u1 = u1 * 0x4c957f2d + 0xf767814f
    u5 = u1 & 0xff
    u1 = u1 * 0x4c957f2d + 0xf767814f & 0xff | 1

    h = ((u1 << 8 | u5) << 8 | u3) << 8 | u4

    param_2[3] = (h >> 24) & 0xff
    param_2[2] = (h >> 16) & 0xff
    param_2[1] = (h >> 8) & 0xff
    param_2[0] = h & 0xff

    if (u4 * u1 - u3 * u5 & 1) == 0:
        param_2[0] = ((l2 | 1) + 2) & 0xff

    for i in range(0, size, 2):
        a1 = param_1[i & 7] ^ doc[i]
        a2 = param_1[(i + 1) & 7] ^ doc[i + 1]

        p1, p2, p3, p4 = param_2
        delta = (p1 * p4 - p2 * p3) & 0xff
        inv = pow(delta, -1, 256)
        x = ((a1 * p4 - p2 * a2) * inv) & 0xff
        y = ((p1 * a2 - a1 * p3) * inv) & 0xff

        print(chr(x), end="")
        print(chr(y), end="")



    

