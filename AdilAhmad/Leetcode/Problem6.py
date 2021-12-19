#Contains Duplicate
class Solution(object):
    def containsDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        distinct = set(nums)
        if (len(nums) == len(distinct)):
            return False
        else:
            return True