import sys


def main():
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    P, V = a[0], a[1]
    Q, M = b[0], b[1]
    
    l1, r1 = P - V, P + V
    l2, r2 = Q - M, Q + M
    
    count1 = r1 - l1 + 1 if l1 <= r1 else l1 - r1 + 1
    count2 = r2 - l2 + 1 if l2 <= r2 else l2 - r2 + 1
    
    intersection = max(0, min(r1, r2) - max(l1, l2) + 1)
    
    res = count1 + count2 - intersection

    print(res)


if __name__ == '__main__':
    main()
