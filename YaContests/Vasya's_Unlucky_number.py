def main():
    with open('Avilov_GIT/YaContests/input.txt', 'r', encoding='utf-8') as fin:
        n, k = map(int, fin.readline().split())
        a = list(map(int, fin.readline().split()))

    INF = 10**30

    best = [INF] * k
    best[0] = 0

    s = 0
    res = 0

    m1 = (0, 0)        
    m2 = (INF, -1)

    for x in a:
        s += x
        r = s % k

        cur = m1 if m1[1] != r else m2
        if cur[0] != INF:
            res = max(res, s - cur[0])

        if s < best[r]:
            best[r] = s

            if r == m1[1]:
                m1 = (s, r)
                if m2[0] < m1[0]:
                    m1, m2 = m2, m1
            elif s < m1[0]:
                m2 = m1
                m1 = (s, r)
            elif s < m2[0]:
                m2 = (s, r)

    with open('Avilov_GIT/YaContests/output.txt', 'w', encoding='utf-8') as fout:
        fout.write(str(res))


if __name__ == '__main__':
    main()