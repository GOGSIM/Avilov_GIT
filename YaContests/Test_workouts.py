def check(a, b, s, ca, cb):
    good = bad = 0
    n = len(s)

    for i in range(n):
        xa = a[i] == s[i]
        xb = b[i] == s[i]

        if xa and xb and a[i] == b[i]:
            good += 1
        elif not xa and not xb and a[i] == b[i]:
            bad += 1

    wa = n - ca
    wb = n - cb

    return (
        good * 2 > ca and
        good * 2 > cb and
        bad * 2 > wa and
        bad * 2 > wb
    )


def solve(n, s, a):
    m = len(a)
    c = [sum(x == y for x, y in zip(t, s)) for t in a]

    res = []

    for i in range(m):
        for j in range(i + 1, m):
            if check(a[i], a[j], s, c[i], c[j]):
                res.append((i + 1, j + 1))

    return res


def main():
    n = int(input())
    s = input().strip()
    m = int(input())
    a = [input().strip() for _ in range(m)]

    res = solve(n, s, a)

    print(len(res))
    for x, y in res:
        print(x, y)


if __name__ == '__main__':
    main()