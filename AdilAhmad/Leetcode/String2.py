# Valid Parentheses

class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        stack = []
        dictionary = {"]":"[", "}":"{", ")":"("}
        for char in s:
            if char in dictionary.values():
                stack.append(char)
            elif char in dictionary.keys():
                if stack == [] or dictionary[char] != stack.pop():
                    return False
            else:
                return False
        return stack == []