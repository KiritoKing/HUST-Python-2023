
if __name__ == '__main__':
    l = [i for i in range(10000, 100000) if str(i * 4) == str(i)[::-1]]
    print(*l)
