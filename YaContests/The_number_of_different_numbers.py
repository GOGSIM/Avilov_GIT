import sys


def main():
    input = sys.stdin.readline
    s = set(map(int, input().split()))
    
    print(len(s))
    

if __name__ == '__main__':
    main()
