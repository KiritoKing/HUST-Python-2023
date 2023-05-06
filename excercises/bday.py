# P3: 相同生日概率

# 具体来说，第一段代码的计算过程中使用了递归调用，每次调用都会将当前问题转化为一个规模更小的问题。这样的计算方式需要使用函数调用栈（function call stack），可能会受到栈深度的限制。

# 而第二段代码的计算过程中使用了循环，每次循环都会重新计算一次概率。这样的计算方式不需要使用函数调用栈，因此可以避免栈溢出的问题。

# 由于计算精度的原因，使用递归计算的结果可能略微偏离精确值。在这种情况下，使用循环计算可能会得到更加精确的结果。因此，两段代码的输出结果可能略微不同。

def bday_problem(n):
    if n == 1:
        return 1
    return (365 - n + 1) / 365 * bday_problem(n - 1)


def bday_problem_no_callstack(n):
    result = 1
    for i in range(1, n):
        result *= (365 - i + 1) / 365
    return result


if __name__ == '__main__':
    N = 100
    print(1-bday_problem(N))
    print(1-bday_problem_no_callstack(N))
