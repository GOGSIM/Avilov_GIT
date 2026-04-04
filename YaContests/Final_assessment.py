def main():
    with open('Avilov_GIT/YaContests/input.txt', 'r', encoding='utf-8') as fin:
        s = fin.readline().strip()
    
    vals = [ord('Z') - ord(c) + 1 for c in s]
    res = min(int(sum(vals) / len(vals) + 0.5), min(vals) + 1)

    with open('Avilov_GIT/YaContests/output.txt', 'w', encoding='utf-8') as fout:
        fout.write(chr(ord('Z') - res + 1))


if __name__ == '__main__':
    main()  