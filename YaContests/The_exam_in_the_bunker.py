import math

INF = 10**18


def check_by_rows(n, r):
    q = n // r
    rem = n % r

    if rem == 0:
        return abs(r - q)

    if abs(rem - (r - rem)) <= 1:
        return abs(r - (q + 1))

    return INF


def check_by_q(n, q):
    best = INF

    if n % q == 0:
        r = n // q
        best = min(best, abs(r - q))

    den = 2 * q + 1

    if n % den == 0:
        t = n // den
        if t > 0:
            r = 2 * t
            best = min(best, abs(r - (q + 1)))

    if n >= q and (n - q) % den == 0:
        t = (n - q) // den
        r = 2 * t + 1
        best = min(best, abs(r - (q + 1)))

    if n >= q + 1 and (n - q - 1) % den == 0:
        t = (n - q - 1) // den
        r = 2 * t + 1
        best = min(best, abs(r - (q + 1)))

    return best


def main():
    with open('Avilov_GIT/YaContests/input.txt', 'r', encoding='utf-8') as fin:
        n = int(fin.readline())

    lim = math.isqrt(n)
    res = INF

    for x in range(1, lim + 1):
        res = min(res, check_by_rows(n, x))
        res = min(res, check_by_q(n, x))

    with open('Avilov_GIT/YaContests/output.txt', 'w', encoding='utf-8') as fout:
        fout.write(str(res))


if __name__ == '__main__':
    main()