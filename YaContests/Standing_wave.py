# O((n+m)log(n))
import sys
from collections import defaultdict


def main():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    start = defaultdict(list)
    finish = defaultdict(list)

    for i in range(n):
        l, r, x = map(int, input().split())
        p = l % 2
        start[l].append((p, x))
        finish[r + 1].append((p, x))

    r_list = [int(input()) for _ in range(m)]

    position = sorted(set(r_list + list(start.keys()) + list(finish.keys())))

    even_sum, odd_sum, q_i = 0, 0, 0
    res = list()

    for pose in position:
        for p, x in start[pose]:
            if p == 0:
                even_sum += x
            else:
                odd_sum += x

        for p, x in finish[pose]:
            if p == 0:
                even_sum -= x
            else:
                odd_sum -= x

        while q_i < m and r_list[q_i] == pose:
            q = r_list[q_i]

            if q % 2 == 0:
                res_sum = even_sum - odd_sum
            else:
                res_sum = odd_sum - even_sum

            res.append(str(res_sum))
            q_i += 1

    print("\n".join(res))


if __name__ == "__main__":
    main()