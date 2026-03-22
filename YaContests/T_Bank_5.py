import sys
from collections import Counter


def main():
    input = sys.stdin.readline
    n = int(input())
    l = list(map(int, input().split()))
    count = Counter(l)
    s = set()
    
    for i in range(n):
        x = l[i]
        y = l[(i + 1) % n]
        z = l[(i + 2) % n]
        
        s.add(min(x, y, z))
        s.add(max(x, y, z))
        
    res = list()
    for x in l:
        ans = n - count[x]
        if x not in s:
            ans += 1
        res.append(str(ans))
        
    print(' '.join(res))        
        

if __name__ == "__main__":
    main()