import random
import bisect
from collections import defaultdict
from typing import List

DEBUG = True


def minimize_diff_greedy(a, b):
    sum_a, sum_b = sum(a), sum(b)
    diff = abs(sum_a - sum_b)
    a_t = sorted(a) if sum_a > sum_b else sorted(b)
    b_t = sorted(b, reverse=True) if sum_a > sum_b else sorted(a, reverse=True)
    i = 0
    while i < len(a_t):
        if a_t[i] < b_t[i]:
            sum_a += b[i] - a[i]
            sum_b += a[i] - b[i]
            t = a_t[i]
            a_t[i] = b_t[i]
            b_t[i] = t
            diff = min(diff, abs(sum_a - sum_b))
            i += 1
        else:
            if DEBUG:
                print("(Greedy) Min Diff =", diff)
            break
    return (a_t, b_t)


def minimize_diff(a: List[int], b: List[int]):
    nums = a + b
    n = len(nums) // 2
    pre = a
    post = b
    if DEBUG:
        print("Pre =", pre)
        print("Post =", post)
    total = sum(nums)
    group_pre = defaultdict(list)
    group_post = defaultdict(list)
    for i in range(1 << n):
        sum_pre = 0
        sum_post = 0
        for j in range(n):
            if i & (1 << j):
                sum_pre += pre[j]
                sum_post += post[j]
        cnt = bin(i).count('1')
        group_pre[cnt].append(sum_pre)
        group_post[cnt].append(sum_post)
    for k in group_post:
        group_post[k].sort()
        group_pre[k].sort()

    ans = float('inf')
    for k in group_pre:
        for sum_pre in group_pre[k]:
            i = bisect.bisect_left(group_post[n - k], (total - 2 * sum_pre) / 2)
            for j in [i - 1, i, i + 1]:
                if 0 <= j < len(group_post[n - k]):
                    ans = min(ans, abs(2 * group_post[n - k][j] + 2 * sum_pre - total))
    if DEBUG:
        print("Min Diff =", ans)
    return (group_post, group_pre)


if __name__ == "__main__":
    n = 10  # 指定列表长度
    a = random.sample(range(100), n)  # 生成随机数列表a
    b = random.sample(range(100), n)  # 生成随机数列表b
    a_t, b_t = minimize_diff(a, b)
    a_t_greedy, b_t_greedy = minimize_diff_greedy(a, b)
