def main():
    with open('Avilov_GIT/YaContests/input.txt', 'r', encoding='utf-8') as fin:
        n = int(fin.readline())
        players = [fin.readline().strip() for _ in range(n)]
        scores = {name: 0 for name in players}

        m = int(fin.readline())
        pred = 0

        for _ in range(m):
            s = fin.readline().split()
            scr = s[0]
            name = s[1]

            a, b = map(int, scr.split(':'))
            cur_t = a + b
            scores[name] += (cur_t - pred)
            pred = cur_t

    res = max(scores, key=scores.get)

    with open('Avilov_GIT/YaContests/output.txt', 'w', encoding='utf-8') as fout:
        fout.write(f'{res} {scores[res]}')


if __name__ == '__main__':
    main()