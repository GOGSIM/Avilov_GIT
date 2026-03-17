import sys


def main():
    A, B, C, D = int(input()), int(input()), int(input()), int(input())
    
    variants = [
        (B + 1, D + 1),
        (A + 1, C + 1),
        (max(A, B) + 1, 1),
        (1, max(C, D) + 1)
    ]
    
    variants = [
        (m, n)
        for m, n in variants
        if m <= A + B and n <= C + D
    ]

    res_m, res_n = min(variants, key=lambda x: (x[0] + x[1], x[0], x[1]))

    print(res_m, res_n)


if __name__ == '__main__':
    main()
