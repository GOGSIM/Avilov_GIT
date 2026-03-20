import sys
import collections


def idx(char):
    if 'a' <= char <= 'z':
        return ord(char) - ord('a')
    return ord(char) - ord('A') + 26

def main():
    with open('Avilov_GIT/YaContests/input.txt', 'r', encoding='utf-8') as fin:
        g, s = map(int, fin.readline().split())
        w = fin.readline().strip()
        z = fin.readline().strip()
        
    need = [0] * 52
    l = [0] * 52

    for char in w:
        need[idx(char)] += 1

    for char in z[:g]:
        l[idx(char)] += 1

    res = 0
    if l == need:
        res += 1

    for i in range(g, s):
        l[idx(z[i - g])] -= 1
        l[idx(z[i])] += 1

        if l == need:
            res += 1

    with open('Avilov_GIT/YaContests/output.txt', 'w', encoding='utf-8') as fout:
        fout.write(str(res))


if __name__ == '__main__':
    main()
