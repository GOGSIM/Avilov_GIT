import sys


def main():
    with open('Avilov_GIT/YaContests/input.txt', 'r', encoding='utf-8') as fin:
        n = int(fin.readline())
        nums = list(map(int, fin.read().split()))
        
    pref = 0
    min_pref = 0
    res = -float('inf')

    for x in nums:
        pref += x
        res = max(res, pref - min_pref)
        min_pref = min(min_pref, pref)
        
    with open('Avilov_GIT/YaContests/output.txt', 'w', encoding='utf-8') as fout:
        fout.write(str(res))


if __name__ == '__main__':
    main()
