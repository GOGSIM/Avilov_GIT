import sys


def main():
    with open('Avilov_GIT/YaContests/input.txt', 'r', encoding='utf-8') as fin:
        n = int(fin.readline())   
        nums = list(map(int, fin.readline().split()))

    MOD = 10**9 + 7
    total = sum(nums)
    l_sum, r_sum, res = 0, total, 0

    for x in nums:
        r_sum -= x
        res = (res + x * l_sum * r_sum) % MOD
        l_sum += x
        
    with open('Avilov_GIT/YaContests/output.txt', 'w', encoding='utf-8') as fout:
        fout.write(str(res % MOD))


if __name__ == '__main__':
    main()
