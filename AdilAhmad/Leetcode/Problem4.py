#Search Insert Position
class Solution(object):
    def searchInsert(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        if ((target in nums) == True):
            return nums.index(target)
        else:
            for i in range(len(nums)):
                if (target < nums[i]):
                    return i - 1