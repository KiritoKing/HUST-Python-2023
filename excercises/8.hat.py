if __name__ == '__main__':
  # A, B, C 戴的帽子颜色分别用 a, b, c 表示，0 表示红色，1 表示白色。
  # 枚举所有可能的帽子颜色组合，找到符合 C 的回答的组合。
  for a in range(2):
      for b in range(2):
          for c in range(2):
              # 如果 A 不知道自己戴的帽子颜色，那么b和c一定不是白色
              if b != 1 and c != 1:
                  # 如果 B 不知道自己戴的帽子颜色，那么a和c一定不是白色
                  if a != 1 and c != 1:
                      # 如果 C 知道自己戴的帽子颜色，那么必须知道 A 和 B 戴的帽子颜色。
                      if (a == b and a != 0) or (a != b):
                          print("A 戴的帽子颜色为", "红色" if a == 0 else "白色")
                          print("B 戴的帽子颜色为", "红色" if b == 0 else "白色")
                          print("C 戴的帽子颜色为", "红色" if c == 0 else "白色")
                          print("")
