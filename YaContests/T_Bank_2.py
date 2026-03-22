def change_count(s: str, word: str) -> list[int]:
    n, m = len(s), len(word)
    return [
        sum(s[i+k] != word[k] for k in range(m))
        for i in range(n - m + 1)
    ]

def main():
    s = input().strip()

    a, b = 'tbank', 'study'
    cost_a = change_count(s, a)
    cost_b = change_count(s, b)
    
    pref = cost_b[:]
    for i in range(1, len(pref)):
        pref[i] = min(pref[i], pref[i-1])
        
    suff = cost_b[:]
    for i in range(1, len(suff)):
        suff[i] = min(suff[i], suff[i-1])
        
    res = float('inf')
    for i in range(len(cost_a)):
        best = float('inf')
        if i - 5 >= 0:
            best = min(best, pref[i-5])
        if i + 5 < len(cost_b):
            best =  min(best, suff[i+5])
        res = min(res, cost_a[i] + best)
    

    print(str(res))

if __name__ == '__main__':
    main()