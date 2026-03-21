def main():
    with open('Avilov_GIT/YaContests/input.txt', 'r', encoding='utf-8') as fin:
        s = fin.readline().strip().split()

    res = []

    for word in s:
        lt = len(word) - len(word.lstrip("'"))
        rt = len(word) - len(word.rstrip("'"))

        core = word.strip("'")
        end = len(core) - rt
        res.append(core[lt:end])

    with open('Avilov_GIT/YaContests/output.txt', 'w', encoding='utf-8') as fout:
        fout.write(''.join(res))

if __name__ == '__main__':
    main()