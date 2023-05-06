import locale
import sys


def minimize_diff(a, b):
    sum_a, sum_b = sum(a), sum(b)
    diff = abs(sum_a - sum_b)
    a, b = sorted(a), sorted(b, reverse=True)
    i = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            sum_a += b[j] - a[i]
            sum_b += a[i] - b[j]
            diff = min(diff, abs(sum_a - sum_b))
            i += 1
            j += 1
        else:
            break
    return diff


if __name__ == "__main__":
    print('sys.stdin.encoding:', sys.stdin.encoding, file=sys.stderr)
    print('locale.getpreferredencoding()', locale.getpreferredencoding(), file=sys.stderr)
