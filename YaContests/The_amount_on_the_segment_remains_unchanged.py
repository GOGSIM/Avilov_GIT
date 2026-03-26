import sys


def main():
    with open('Avilov_GIT/YaContests/input.txt', 'r', encoding='utf-8') as fin:
        n = int(fin.readline())
        A = list(map(int, fin.readline().split()))
        Q = int(fin.readline())
        X = int(fin.readline())
        
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + A[i]
    
    res = 0
    
    for _ in range(Q):
        x1 = X
        X = (11173 * X  + 1) % 1000000007
        x2 = X
        X = (11173 * X  + 1) % 1000000007
        
        l = min(x1 % n, x2 % n)
        r = max(x1 % n, x2 % n)
        
        res += pref[r+1] - pref[l]
        
    with open('Avilov_GIT/YaContests/output.txt', 'w', encoding='utf-8') as fout:
        fout.write(str(res % 1000000007))


if __name__ == '__main__':
    main()
