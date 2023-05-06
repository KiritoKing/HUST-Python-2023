# P6: 三个孩子的年龄

if __name__ == "__main__":
    possible = []
    product = 36
    for i in range(1, product+1):
        for j in range(i, product+1):
            for k in range(j, product+1):
                if i * j * k == product:
                    possible.append((i, j, k))

    res = []
    for i, tup in enumerate(possible):
        sum = tup[0] + tup[1] + tup[2]
        for j in range(i+1, len(possible)):
            if sum == possible[j][0] + possible[j][1] + possible[j][2]:
                if (len(res) == 0):
                    res.append(tup)
                res.append(possible[j])

    for r in res:
        if r[2] != r[1]: # 最大值唯一
            print(*r)
    