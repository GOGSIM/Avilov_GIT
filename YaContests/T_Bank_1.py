def main():
    s = input().strip()

    res = sorted(s)
    for i in range(len(res)):
        if res[i] != '0':
            res[0], res[i] = res[i], res[0]
            break
    

    print(''.join(res))

if __name__ == '__main__':
    main()