import sys

def get_p_n(k, x, m):
    countk = x * m
    
    p = (k-1) // countk + 1
    k_in = (k-1) % countk
    count_n = k_in // x + 1
    
    return p, count_n
       
def main():
    l = list(map(int, input().split()))
    k1, m, k2, p2, n2 = l[0], l[1], l[2], l[3], l[4]
    possible = list()

    for x in range(1, k1+k2+1):
        p, n = get_p_n(k2, x, m)
        
        if p == p2 and n == n2:
            p1 = (k1-1) // (x*m) + 1
            n1 = ((k1-1) % (x*m)) // x + 1
            possible.append((p1, n1))
            
    if len(possible) == 0:
        print(-1, -1)
        return 
    
    p_set = set()
    n_set = set()
    
    for p1, n1 in possible:
        p_set.add(p1)
        n_set.add(n1)
        
    if len(p_set) == 1:
        res_p = next(iter(p_set))
    else:
        res_p = 0
        
    if len(n_set) == 1:
        res_n = next(iter(n_set))
    else:
        res_n = 0
        
    print(res_p, res_n)
        

if __name__ == '__main__':
    main()
