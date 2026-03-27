def main():
    with open('Avilov_GIT/YaContests/input.txt', 'r', encoding='utf-8') as fin:
        s = fin.readline().strip()

    n = len(s)

    pos = [[] for _ in range(26)]
    for i, ch in enumerate(s):
        pos[ord(ch) - ord('a')].append(i)

    max_cnt = max(len(lst) for lst in pos)

    mod1 = 10**9 + 7
    mod2 = 10**9 + 9
    base = 911382323

    p1 = [1] * (n + 1)
    p2 = [1] * (n + 1)
    h1 = [0] * (n + 1)
    h2 = [0] * (n + 1)

    for i in range(n):
        x = ord(s[i]) - ord('a') + 1
        p1[i + 1] = (p1[i] * base) % mod1
        p2[i + 1] = (p2[i] * base) % mod2
        h1[i + 1] = (h1[i] * base + x) % mod1
        h2[i + 1] = (h2[i] * base + x) % mod2

    def get_hash(l, r):
        x1 = (h1[r] - h1[l] * p1[r - l]) % mod1
        x2 = (h2[r] - h2[l] * p2[r - l]) % mod2
        return x1, x2

    def all_equal(positions, length):
        first = get_hash(positions[0], positions[0] + length)
        for p in positions[1:]:
            if get_hash(p, p + length) != first:
                return False
        return True

    ans = 1

    for lst in pos:
        if len(lst) != max_cnt:
            continue

        if len(lst) == 1:
            ans = max(ans, n - lst[0])
            continue

        min_gap = n
        for i in range(len(lst) - 1):
            min_gap = min(min_gap, lst[i + 1] - lst[i])

        max_possible = min(min_gap, n - lst[-1])

        left, right = 1, max_possible
        best = 1

        while left <= right:
            mid = (left + right) // 2
            if all_equal(lst, mid):
                best = mid
                left = mid + 1
            else:
                right = mid - 1

        ans = max(ans, best)

    with open('Avilov_GIT/YaContests/output.txt', 'w', encoding='utf-8') as fout:
        fout.write(str(ans))


if __name__ == '__main__':
    main()