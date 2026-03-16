import sys


def main():
    s = list(map(int, input().split()))
    s.sort()
    res = list()
    
    if s[-1] * s[-2] > s[0] * s[1]:
        res.append(s[-1])
        res.append(s[-2])
    else:
        res.append(s[0])
        res.append(s[1])

    res.sort()
    print(*res)
    

if __name__ == '__main__':
    main()
