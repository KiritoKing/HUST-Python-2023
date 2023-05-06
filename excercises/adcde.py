# P4: 寻找五位数abcde,乘以4以后变成edcba

if __name__ == '__main__':
    l = [i for i in range(10000, 100000) if str(i * 4) == str(i)[::-1]]
    print(*l)
