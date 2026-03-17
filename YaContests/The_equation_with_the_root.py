import sys


def main():
    a, b, c = int(input()), int(input()), int(input())
    
    if c < 0:
        print('NO SOLUTION')
        return

    if a == 0:
        if b == c**2:
            print('MANY SOLUTIONS')
        else:
            print('NO SOLUTION')
        return

    num = c**2 - b
    if num % a != 0:
        print('NO SOLUTION')
        return

    x = int(num / a)
    print(x)
    

if __name__ == '__main__':
    main()