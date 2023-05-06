# P2: 青蛙跳台阶问题

def fib(n, dp):
    if n == 1:
        return 1
    if n == 2:
        return 2
    if dp[n] != 0:
        return dp[n]
    dp[n] = fib(n - 1, dp) + fib(n - 2, dp)
    return dp[n]



if __name__ == '__main__':
    N = 100
    dp = [0] * (N+1)
    print(fib(N, dp))
