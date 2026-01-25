class Solution(object):
    def twoSum(self, nums, target):
        s = {}

        for i, n in enumerate(nums):
            x = target - n
            if x in s:
                return [s[x], i]
            s[n] = i

