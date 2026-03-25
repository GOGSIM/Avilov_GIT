def max_pref(a, b):
    i, m = 0, min(len(a), len(b))
    while i < m and a[i] == b[i]:
        i += 1
    return i


def main():
    with open('Avilov_GIT/YaContests/input.txt', 'r', encoding='utf-8') as fin:
        n = int(fin.readline())
        words = [fin.readline().strip() for _ in range(n)]

    words.sort()
    res = len(words[0])

    for i in range(0, n, 2):
        res = min(res, max_pref(words[i], words[i + 1]))

    with open('Avilov_GIT/YaContests/output.txt', 'w', encoding='utf-8') as fout:
        fout.write(str(res))


if __name__ == '__main__':
    main()