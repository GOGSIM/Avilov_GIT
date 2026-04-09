def check(s, start):
    n = len(s)
    st = []
    mp = {')': '(', ']': '[', '}': '{'}

    for i in range(n):
        c = s[(start + i) % n]

        if c in '([{':
            st.append(c)
        else:
            if not st or st[-1] != mp[c]:
                return False
            st.pop()

    return not st


def solve(s):
    n = len(s)

    if n == 0:
        return 'YES'

    if n % 2:
        return 'NO'

    for i in range(n):
        if check(s, i):
            return 'YES'

    return 'NO'


def main():
    s = input().strip()
    print(solve(s))


if __name__ == '__main__':
    main()