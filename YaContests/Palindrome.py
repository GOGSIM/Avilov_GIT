import sys
import collections

def main():
    with open('Avilov_GIT/YaContests/input.txt', 'r', encoding='utf-8') as fin:
        n = int(fin.readline())
        s = fin.readline().strip()
        
    count = collections.Counter(s)
    left, mid = list(), ''
    
    for char in sorted(count):
        left.append(char * (count[char]//2))
     
    for char in sorted(count):   
        if count[char] % 2 == 1:
            mid = char
            break
        
    l_part = ''.join(left)
    res = l_part + mid + l_part[::-1]
    
    with open('Avilov_GIT/YaContests/output.txt', 'w', encoding='utf-8') as fout:
        fout.write(res)
        

if __name__ == '__main__':
    main()
