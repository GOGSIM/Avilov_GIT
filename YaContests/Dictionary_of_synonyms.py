import sys


def main():
    input = sys.stdin.readline
    n = int(input())
    d = dict()
    
    for _ in range(n):
        a, b = input().split()
        d[a] = b
        d[b] = a
        
    key = input().strip()
    
    print(d[key])
    

if __name__ == '__main__':
    main()
