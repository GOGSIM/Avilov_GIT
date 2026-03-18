import sys


def main():
    input = sys.stdin.readline
    n = int(input())
    
    all_lang = set()
    popular_lang = None
    
    for _ in range(n):
        m = int(input())
        lang = set()
        
        for _ in range(m):
            lang.add(input().strip())
            
        if popular_lang is None:
            popular_lang = lang.copy()
        else:
            popular_lang &= lang    
            
        all_lang |= lang
            
    print(len(popular_lang))
    for lang in sorted(popular_lang):
        print(lang)
            
    print(len(all_lang))
    for lang in sorted(all_lang):
        print(lang)


if __name__ == '__main__':
    main()