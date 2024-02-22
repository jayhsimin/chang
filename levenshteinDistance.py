def levenshtein_distance(s1, s2):
    m, n = len(s1), len(s2)

    # 初始化一個二維矩陣，用於存儲子問題的解
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 初始化第一行和第一列
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # 填充矩陣，根據子問題的解計算當前問題的解
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1,      # 刪除
                           dp[i][j - 1] + 1,      # 插入
                           dp[i - 1][j - 1] + cost)  # 替換

    # 返回最終的編輯距離
    return dp[m][n]

# 測試
s1 = [11, 5, 6, 7, 2, 1, 4, 9, 3, 10, 12, 2]
s2 = [4, 5, 6, 7, 2, 1, 12, 9, 3, 8, 11, 2]
distance = levenshtein_distance(s1, s2)
print(f"Levenshtein Distance: {distance}")
