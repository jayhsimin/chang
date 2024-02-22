def hamming_distance(s1, s2):
    # 確保兩個字串等長
    if len(s1) != len(s2):
        raise ValueError("Input strings must have the same length")

    # 初始化Hamming Distance為0
    distance = 0

    # 遍歷兩個字串，比較對應位置上的元素是否相等
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            distance += 1

    return distance

# 測試
s1 = [11, 5, 6, 7, 2, 1, 4, 9, 3, 10, 12, 2]
s2 = [4, 5, 6, 7, 2, 1, 4, 9, 3, 8, 11, 2]
distance = hamming_distance(s1, s2)
print(f"Hamming Distance: {distance}")
