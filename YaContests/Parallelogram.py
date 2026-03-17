import sys

def same_diag(a, b, c, d):
    return a[0] + b[0] == c[0] + d[0] and a[1] + b[1] == c[1] + d[1]

def main():
    input = sys.stdin.readline
    n = int(input())
    
    for _ in range(n):
        coordinates = list(map(int, input().split()))
        
        k1 = (coordinates[0], coordinates[1])
        k2 = (coordinates[2], coordinates[3])
        k3 = (coordinates[4], coordinates[5])
        k4 = (coordinates[6], coordinates[7])
        
        if (
            same_diag(k1, k2, k3, k4) or
            same_diag(k1, k3, k2, k4) or
            same_diag(k1, k4, k2, k3)
        ):
            print('YES')
        else: 
            print('NO')
        

if __name__ == '__main__':
    main()
