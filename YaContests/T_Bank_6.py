import sys
import random

sys.setrecursionlimit(10**7)
input = sys.stdin.readline


class Uz:
    def __init__(self, l, r, left=None, right=None):
        self.l = l          
        self.r = r          
        self.left = left
        self.right = right
        self.pr = random.randint(1, 10**9)
        self.sz = 0
        self.update()

    def dlina(self):
        return self.r - self.l + 1

    def update(self):
        self.sz = self.dlina()
        if self.left:
            self.sz += self.left.sz
        if self.right:
            self.sz += self.right.sz


def razmer(t):
    return t.sz if t else 0


def kopiya(t):
    if not t:
        return None
    new = Uz(t.l, t.r, t.left, t.right)
    new.pr = t.pr
    new.sz = t.sz
    return new


def merge(a, b):
    if not a:
        return b
    if not b:
        return a

    if a.pr > b.pr:
        a = kopiya(a)
        a.right = merge(a.right, b)
        a.update()
        return a
    else:
        b = kopiya(b)
        b.left = merge(a, b.left)
        b.update()
        return b


def split(t, k):
    if not t:
        return None, None

    left_sz = razmer(t.left)
    cur_len = t.dlina()

    if k < left_sz:
        a, b = split(t.left, k)
        t = kopiya(t)
        t.left = b
        t.update()
        return a, t

    if k > left_sz + cur_len:
        a, b = split(t.right, k - left_sz - cur_len)
        t = kopiya(t)
        t.right = a
        t.update()
        return t, b

    take = k - left_sz

    if take == 0:
        right_part = Uz(t.l, t.r, None, t.right)
        right_part.pr = t.pr
        right_part.update()
        return t.left, right_part

    if take == cur_len:
        left_part = Uz(t.l, t.r, t.left, None)
        left_part.pr = t.pr
        left_part.update()
        return left_part, t.right

    mid = t.l + take - 1

    left_block = Uz(t.l, mid)
    right_block = Uz(mid + 1, t.r)

    left_tree = merge(t.left, left_block)
    right_tree = merge(right_block, t.right)

    return left_tree, right_tree


def kth(t, k, s):
    left_sz = razmer(t.left)
    cur_len = t.dlina()

    if k <= left_sz:
        return kth(t.left, k, s)

    if k <= left_sz + cur_len:
        pos = k - left_sz - 1
        return s[t.l + pos]

    return kth(t.right, k - left_sz - cur_len, s)


def main():
    n, q = map(int, input().split())
    s = input().strip()

    koren = Uz(0, n - 1)

    otv = []

    for _ in range(q):
        zapros = list(map(int, input().split()))

        if zapros[0] == 1:
            l, r = zapros[1], zapros[2]
            dl = r - l + 1

            A, BC = split(koren, l - 1)
            B, C = split(BC, dl)

            koren = merge(A, merge(B, merge(B, C)))

        else:
            i = zapros[1]
            otv.append(kth(koren, i, s))

    print("\n".join(otv))


if __name__ == "__main__":
    main()