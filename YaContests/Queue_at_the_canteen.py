def main():
    with open('Avilov_GIT/YaContests/input.txt', 'r', encoding='utf-8') as fin:
        cases = int(fin.readline())
        answers = []

        for _ in range(cases):
            n, d = map(int, fin.readline().split())

            wait = 0
            last_bad = 0

            for i in range(1, n + 1):
                t, k = map(int, fin.readline().split())

                if wait + d > t:
                    last_bad = i

                wait += k

            answers.append(str(last_bad + 1))

    with open('Avilov_GIT/YaContests/output.txt', 'w', encoding='utf-8') as fout:
        fout.write('\n'.join(answers))


if __name__ == '__main__':
    main()