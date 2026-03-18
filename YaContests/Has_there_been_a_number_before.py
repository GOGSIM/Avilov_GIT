import sys


def main():
    s = set()

    for x in map(int, input().split()):
        print("YES" if x in s else "NO")
        s.add(x)


if __name__ == '__main__':
    main()
