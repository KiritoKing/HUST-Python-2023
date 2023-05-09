def hanoi(n, source, target, auxiliary):
    if n > 0:
        hanoi(n-1, source, auxiliary, target)
        print("Move disk %d from %s to %s" % (n, source, target))
        hanoi(n-1, auxiliary, target, source)

if (__name__ == '__main__'):
    # 示例用法
    hanoi(3, 'A', 'C', 'B')
