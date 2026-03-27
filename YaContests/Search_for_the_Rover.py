import sys


def main():
    with open('Avilov_GIT/YaContests/input.txt', 'r', encoding='utf-8') as fin:
        n = int(fin.readline())

        left_b = -10**18
        right_b = 10**18
        
        for _ in range(n):
            x, d = map(int, fin.readline().split())
            left_b = max(left_b, x - d)
            right_b = min(right_b, x + d)
        
    with open('Avilov_GIT/YaContests/output.txt', 'w', encoding='utf-8') as fout:
        fout.write('-1' if left_b > right_b else str(right_b))


if __name__ == '__main__':
    main()
