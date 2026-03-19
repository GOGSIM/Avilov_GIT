import sys


def flexion(x, lim):
    if x <= lim: return 0
    need = (x + lim - 1) // lim
    
    return (need - 1).bit_length()

def main():
    n, m, h, w = map(int, sys.stdin.readline().split())

    res = min(
        flexion(n, w) + flexion(m, h),
        flexion(n, h) + flexion(m, w)
    )

    print(res)
    

if __name__ == '__main__':
    main()