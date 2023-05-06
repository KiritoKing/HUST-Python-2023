# P1: 阶乘问题

def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)

def factorial_no_callstack(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

if __name__ == '__main__':
    N = 100
    print(factorial(N))
    print(factorial_no_callstack(N))
