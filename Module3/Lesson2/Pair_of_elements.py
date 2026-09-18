class PairOfElements:
    def two_sum(self, nums, target):
        lookup = {}
        for i, num in enumerate(nums):
            print("i = ", i, "num = ", num)
            if target - num in lookup:
                print("Pair found at index", lookup[target - num], i)
                return 
            lookup[num] = i
            
value = int(input("Enter the target value: "))
obj1 = PairOfElements()
nums = (10, 20, 30, 40, 50, 60, 70)
obj1.two_sum(nums, value)
        