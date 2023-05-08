from random import random

PI = 3.141592653589793238462643383279502884197169399375105820974944592307816406286


def monte_carno(n):
    hits = 0
    for i in range(1, n + 1):
        x, y = random(), random()
        if x * x + y * y <= 1:
            hits += 1
    return 4.0 * hits / n


if __name__ == '__main__':
    pi = 0
    while abs(pi - PI) > 0.001:
        pi = monte_carno(1000000)
    print(pi)
