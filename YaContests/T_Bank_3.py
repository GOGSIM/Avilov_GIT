def main():
    t = int(input())
    
    for _ in range(t):
        s = input().strip()
        ss = s + s
        cur, maxi = 0, 0
        
        for bit in ss:
            if bit == '1':
                cur += 1
                if cur > maxi:
                    maxi = cur
            else:
                cur = 0
                
        if maxi > len(s):
            maxi = len(s)
                
        if maxi == 0:
            print(0)
        elif maxi == len(s):
            print(len(s) * len(s))
        else:
            x = (maxi+1) // 2
            y = maxi + 1 - x
            print(x * y)
    
    
if __name__ == '__main__':
    main()