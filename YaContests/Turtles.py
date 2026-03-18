import sys


def main():
    input = sys.stdin.readline
    n = int(input())
    true = set()
    
    for _ in range(n):
        a, b = map(int, input().split())
        
        if a >= 0 and b >= 0 and a + b == n-1:
            true.add((a, b))
            
    res = {}
    for a, b in true:
        res[a+b] = res.get(a+b, 0) + 1
        
    print(max(res.values(), default=0))
         

if __name__ == '__main__':
    main()
