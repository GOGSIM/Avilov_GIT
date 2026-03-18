import sys


def main():
    input = sys.stdin.readline

    a = set(map(int, input().split()))
    b = set(map(int, input().split()))

    res = sorted(a & b)

    print(*res)


if __name__ == "__main__":
    main()