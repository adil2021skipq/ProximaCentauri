#Problem 3 - Remove Element
class Solution(object):
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        length = len(nums)
        for i in range(len(nums)):
            if (nums[i] == val):
                nums.remove(nums[i])
                nums.append(0)
                length -= 1
        return length