import sys


def main():
    street = list(map(int, input().split()))
    to_west, to_east = [0]*10, [0]*10
    res = 0
    
    shop_pose = -float('inf')
    for i in range(10):
        if street[i] == 2:
            shop_pose = i
        to_west[i] = i - shop_pose
            
    shop_pose = float('inf')
    for i in range(9, -1, -1):
        if street[i] == 2:
            shop_pose = i
        to_east[i] = shop_pose - i
            
    for i in range(10):
        if street[i] == 1:
            lengh = min(to_west[i], to_east[i])
            res = max(res, lengh)
            
    print(res)


if __name__ == '__main__':
    main()
