import sys


def main():
    input = sys.stdin.readline
    d = dict()
    
    while True:
        try:
            name, prod, count = input().split()
            count = int(count)
            
            if name not in d:
                d[name] = dict()
                
            if prod not in d[name]:
                d[name][prod] = 0
                
            d[name][prod] += count
            
        except:
            break
        
    for name in sorted(d):
        print(name + ":")
        for prod in sorted(d[name]):
            print(prod, d[name][prod])
    

if __name__ == '__main__':
    main()
