class Solution:
    def calPoints(self, operations):
        stack = []
        for c in operations:
            if c == "+":
                stack.append(stack[-1] + stack[-2])
            elif c == "D":
                stack.append(stack[-1] * 2)
            elif c == "C":
                stack.pop()
            else:
                stack.append(int(c))
        return sum(stack)
        
def main():
    sol = Solution()
    ops = ["1","2","+","C","5","D"]
    print(sol.calPoints(ops))

if __name__ == "__main__":
    main()


# https://neetcode.io/problems/baseball-game?list=neetcode250