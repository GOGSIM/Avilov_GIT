import sys


def main():
    with open('Avilov_GIT/YaContests/input.txt', 'r', encoding='utf-8') as fin:
        n, k = map(int, fin.readline().split())   
        nums = list(map(int, fin.readline().split()))
        
    l, suma, res = 0, 0, 0
    for r in range(n):
        suma += nums[r]
        
        while suma > k:
            suma -= nums[l]
            l += 1
            
        if suma == k:
            res += 1
        
    with open('Avilov_GIT/YaContests/output.txt', 'w', encoding='utf-8') as fout:
        fout.write(str(res))


if __name__ == '__main__':
    main()
