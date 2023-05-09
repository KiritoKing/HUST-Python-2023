if __name__ == '__main__':
    hats = ['red', 'red', 'red', 'white', 'white'] # 红帽子和白帽子的列表

    for i in range(len(hats)):
        a_hat = hats[i] # A戴帽子
        b_hat = hats[(i+1)%len(hats)] # B戴帽子
        c_hat = hats[(i+2)%len(hats)] # C戴帽子
        # 如果A和B都不知道自己帽子的颜色，那么C一定戴红色的帽子
        if a_hat != b_hat and b_hat != c_hat:
            print("C戴的是%s帽子" % c_hat)
            break
