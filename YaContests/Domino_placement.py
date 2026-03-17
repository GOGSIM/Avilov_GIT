import sys

def main():
    n, m = map(int, input().split())
    placement = [sys.stdin.readline().strip() for _ in range(n)]
    res = 0

    for i in range(n):
        for j in range(m):
            if placement[i][j] == '.':
                if j + 1 < m and placement[i][j + 1] == '.':
                    res += 1
                if i + 1 < n and placement[i + 1][j] == '.':
                    res += 1

    print(res)

if __name__ == '__main__':
    main()