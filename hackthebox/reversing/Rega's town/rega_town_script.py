import string

def main():
    letters = string.ascii_letters
    digits = string.digits
    upper_case = string.ascii_uppercase

    for c1 in ['X', 'Y', 'Z']:
        for c2 in digits:
            for c3 in letters:
                if ord(c1) * ord(c2) * ord(c3) == 499824:
                    print(f"Block 1 found: {c1}{c2}{c3}")

    for c1 in ['A']:
        for c2 in letters:
            for c3 in digits:
                if ord(c1) * ord(c2) * ord(c3) == 377910:
                    print(f"Block 2 found: {c1}{c2}{c3}")

    for c1 in ['T']:
        for c2 in ['h', '7']:
            for c3 in digits:
                if ord(c1) * ord(c2) * ord(c3) == 445536:
                    print(f"Block 3 found: {c1}{c2}{c3}")

    for c1 in upper_case:
        for c2 in digits:
            for c3 in ['n']:
                for c4 in ['a','b','c','d','e','f','g','h']:
                    if ord(c1) * ord(c2) * ord(c3) * ord(c4) == 41637750:
                        print(f"Block 4 found: {c1}{c2}{c3}{c4}")

    for c1 in ['O']:
        for c2 in digits:
            if ord(c1) * ord(c2) == 4345:
                print(f"Block 5 found: {c1}{c2}")

    for c1 in letters:
        for c2 in letters:
            for c3 in letters:
                if ord(c1) * ord(c2) * ord(c3) == 882336:
                    word = f"{c1}{c2}{c3}"
                    if word == "The":
                        print(f"Block 6 found: {word}")

    range_nx = ['n','o','p','q','r','s','t','u','v','w','x']
    for c1 in upper_case:
        for c2 in range_nx:
            for c3 in range_nx:
                for c4 in ['n', 'c']:
                    if ord(c1) * ord(c2) * ord(c3) * ord(c4) == 122051160:
                        print(f"Block 7 found: {c1}{c2}{c3}{c4}")

if __name__ == "__main__":
    main()

