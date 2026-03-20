import sys


def main():
    accounts = dict()
    
    for s in sys.stdin:
        line = s.split()
        cmd = s[0]
        
        if cmd == "DEPOSIT":
            name = line[1]
            sum = int(line[2])
            accounts[name] = accounts.get(name, 0) + sum            
        
        elif cmd == "WITHDRAW":
            name = line[1]
            sum = int(line[2])
            accounts[name] = accounts.get(name, 0) - sum
        
        elif cmd == "BALANCE":
            name = line[1]
            print(accounts[name] if name in accounts else "ERROR")
        
        elif cmd == "TRANSFER":
            name1, name2 = line[1], line[2]
            sum = int(line[3])
            
            accounts[name1] = accounts.get(name1, 0) - sum
            accounts[name2] = accounts.get(name2, 0) + sum
        
        elif cmd == "INCOME":
            p = int(line[1])
            for name in accounts:
                if accounts[name] > 0:
                    accounts[name] += accounts[name] * p // 100


if __name__ == '__main__':
    main()
