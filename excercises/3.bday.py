# Specifically, the calculation process in the first code snippet uses recursive calls, with each call transforming the current problem into a smaller-sized problem.
# This calculation method requires the use of a function call stack, which may be limited by stack depth.
# In contrast, the calculation process in the second code snippet uses a loop, with each iteration recalculating the probability. 
# This calculation method does not require the use of a function call stack, and thus can avoid stack overflow issues.
# Due to the precision of the calculation, the result obtained by recursive computation may deviate slightly from the exact value.
# In such cases, using a loop calculation may yield a more accurate result. Therefore, the output results of the two code snippets may differ slightly.

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
    print(1 - bday_problem(N))
    print(1 - bday_problem_no_callstack(N))
