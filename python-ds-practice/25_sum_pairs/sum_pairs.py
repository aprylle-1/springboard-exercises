def sum_pairs(nums, goal):
    """Return tuple of first pair of nums that sum to goal.

    For example:

        >>> sum_pairs([1, 2, 2, 10], 4)
        (2, 2)

    (4, 2) sum to 6, and come before (5, 1):

        >>> sum_pairs([4, 2, 10, 5, 1], 6) # (4, 2)
        (4, 2)

    (4, 3) sum to 7, and finish before (5, 2):

        >>> sum_pairs([5, 1, 4, 8, 3, 2], 7)
        (4, 3)

    No pairs sum to 100, so return empty tuple:

        >>> sum_pairs([11, 20, 4, 2, 1, 5], 100)
        ()
    """
    curr_pair = [[len(nums) + 1, len(nums) + 1],[len(nums) + 1, len(nums) + 1]]
    pair = []
    pair_index = []
    for num in nums:
        to_add = goal - num
        if nums.count(to_add) == 1 and nums.index(to_add) > nums.index(num):
            pair = [num, to_add]
            pair_index = [nums.index(num), nums.index(to_add)]
        elif nums.count(to_add) > 1:
            curr_index = 0
            for x in range(len(nums)):
                if nums[x] == to_add and x > curr_index:
                    curr_index = x
            pair = [num, to_add]
            pair_index = [nums.index(num), curr_index]
        else:
            pair = [len(nums) + 1, len(nums) + 1]
            pair_index = [len(nums) + 1, len(nums) + 1]
        if pair_index[1] < curr_pair[1][1]:
            curr_pair[0] = pair
            curr_pair[1] = pair_index
    if curr_pair == [[len(nums) + 1, len(nums) + 1],[len(nums) + 1, len(nums) + 1]]:
        return ()
    else:
        return (curr_pair[0][0],curr_pair[0][1])