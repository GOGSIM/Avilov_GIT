MOD = 10**9 + 7


def poschitat_dlya_tsveta(dlini, k):
    dlini.sort()
    dp = [0] * (k + 1)
    dp[0] = 1

    obrabotano = 0
    for d in dlini:
        obrabotano += 1
        for j in range(min(obrabotano, k), 0, -1):
            svobodnyh = d - (j - 1)
            if svobodnyh > 0:
                dp[j] = (dp[j] + dp[j - 1] * svobodnyh) % MOD

    return dp


def main():
    n, k = map(int, input().split())

    if n == 1:
        print(1 if k == 1 else 0)
        return

    if k > 2 * n - 2:
        print(0)
        return

    dlini_1 = []
    dlini_2 = []

    for x in range(-(n - 1), n):
        dlina = n - abs(x)
        if x % 2 == 0:
            dlini_1.append(dlina)
        else:
            dlini_2.append(dlina)

    ways1 = poschitat_dlya_tsveta(dlini_1, k)
    ways2 = poschitat_dlya_tsveta(dlini_2, k)

    otvet = 0
    for i in range(k + 1):
        otvet = (otvet + ways1[i] * ways2[k - i]) % MOD

    print(otvet)


if __name__ == "__main__":
    main()