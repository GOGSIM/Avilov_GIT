import sys


def main():
    troom, tcond = map(int, input().split())
    mode = input().strip()
    res = 0
    if mode == 'freeze':
        res = min(troom, tcond)
    elif mode == 'heat':
        res = max(troom, tcond)
    elif mode == 'auto':
        if troom < tcond:
            res = max(troom, tcond)
        elif troom == tcond:
            res = tcond
        else:
            res = min(troom, tcond)
    else:
        res = troom
        
    print(res)
    

if __name__ == '__main__':
    main()
