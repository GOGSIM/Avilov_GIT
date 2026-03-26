import sys


def main():
    with open('Avilov_GIT/YaContests/input.txt', 'r', encoding='utf-8') as fin:
        n = int(fin.readline())
        nums = list(map(int, fin.read().split()))
        
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i+1] = pref[i] + int(nums[i])   
        
    with open('Avilov_GIT/YaContests/output.txt', 'w', encoding='utf-8') as fout:
        fout.write(" ".join(map(str, pref[1:])))


if __name__ == '__main__':
    main()
