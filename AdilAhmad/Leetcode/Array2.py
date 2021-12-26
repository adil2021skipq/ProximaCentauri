#Problem 2 - Remove Duplicates from Sorted Array
class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        length = len(nums)
        for i in range(1, len(nums)):
            if (nums[i] == nums[i-1]):
                nums.remove(nums[i])
                nums.append(0)
                length -= 1
        return length