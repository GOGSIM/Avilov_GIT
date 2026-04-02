def main():
    with open('Avilov_GIT/YaContests/input.txt', 'r', encoding='utf-8') as fin:
        commands = str(fin.readline())
        
    x = y = 0
    visited = {(0, 0)}
    repeated = set()
    
    moves = {
        'U': (0, 1),
        'D': (0, -1),
        'R': (1, 0),
        'L': (-1, 0)
    }
    
    for move in commands:
        dx, dy = moves[move]
        x += dx
        y += dy
        cur = (x, y)
        
        if cur in visited:
            repeated.add(cur)
        else:
            visited.add(cur)
    

    with open('Avilov_GIT/YaContests/output.txt', 'w', encoding='utf-8') as fout:
        fout.write(str(len(repeated)))


if __name__ == '__main__':
    main()