class Solution(object):
    def numDistinct(self, s, t):
        n, m = len(s), len(t)

        if m > n:
            return 0
        if m == 0:
            return 1

        res = [0] * (m + 1)
        res[0] = 1

        for i in range(n):
            limit = min(i + 1, m)
            for j in range(limit - 1, -1, -1):
                if s[i] == t[j]:
                    res[j + 1] += res[j]

        return res[m]