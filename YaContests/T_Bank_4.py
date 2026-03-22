from collections import deque


def bfs(start, graph, n, best):
    d = [-1] * (n + 1)
    parent = [-1] * (n + 1)

    q = deque([start])
    d[start] = 0

    res = best
    
    while q:
        u = q.popleft()
        
        if d[u] * 2 + 1 >= res:
            continue
        
        for v in graph[u]:
            if d[v] == -1:
                d[v] = d[u] + 1
                parent[v] = u
                q.append(v)
            elif parent[u] != v:
                clen = d[u] + d[v] + 1
                if clen < res:
                    res = clen
                    
    return res
                
def main():
    n, m = map(int, input().split())
    graph = [list() for _ in range(n + 1)]
    
    for _ in range(m):
        a, b = map(int, input().split())
        graph[a].append(b)
        graph[b].append(a)
        
    res = float('inf')
    
    for start in range(1, n+1):
        res = bfs(start, graph, n, res)
        if res == 3:
            break
        
    print(-1 if res == float('inf') else res)
    

if __name__ == '__main__':
    main()