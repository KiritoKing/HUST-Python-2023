# P3: 相同生日概率

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
