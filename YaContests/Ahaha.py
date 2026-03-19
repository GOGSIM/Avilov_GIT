import sys

def main():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    res, cur = 0, 0

    for i, char in enumerate(s):
        if char != 'h' and char != 'a':
            cur = 0
        elif s[i - 1] != char and i > 0 and (s[i - 1] == 'h' or s[i - 1] == 'a'):
            cur += 1
        else:
            cur = 1

        if cur > res:
            res = cur

    print(res)

if __name__ == '__main__':
    main()