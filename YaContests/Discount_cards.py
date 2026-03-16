import sys


def main():
    N, C, R = map(int, input().split())
    lost_num = list(map(int, input().split()))
    reserve_num = list(map(int, input().split()))

    has_lost = [False] * (N + 2)
    has_reserve = [False] * (N + 2)

    for i in lost_num:
        has_lost[i] = True

    for i in reserve_num:
        has_reserve[i] = True

    for i in range(1, N + 1):
        if has_lost[i] and has_reserve[i]:
            has_lost[i] = False
            has_reserve[i] = False

    res = N

    for i in range(1, N + 1):
        if has_lost[i]:
            if has_reserve[i - 1]:
                has_reserve[i - 1] = False
                has_lost[i] = False
            elif has_reserve[i + 1]:
                has_reserve[i + 1] = False
                has_lost[i] = False
            else:
                res -= 1

    print(res)


if __name__ == '__main__':
    main()