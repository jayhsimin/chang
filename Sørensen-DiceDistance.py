def sorensen_dice_coefficient(s1, s2):
    # 確保兩個字串等長
    if len(s1) != len(s2):
        raise ValueError("Input strings must have the same length")

    # 將字串視為集合
    set1 = set(s1)
    set2 = set(s2)

    # 計算交集的元素個數
    intersection_size = len(set1.intersection(set2))

    # 計算Sørensen-Dice係數
    dice_coefficient = (2.0 * intersection_size) / (len(set1) + len(set2))

    return dice_coefficient

# 測試
s1 = [11, 5, 6, 7, 2, 1, 4, 9, 3, 10, 12, 2]
s2 = [4, 5, 6, 7, 2, 1, 4, 9, 3, 8, 11, 2]
coeff = sorensen_dice_coefficient(s1, s2)
print(f"Sørensen-Dice係數: {coeff}")
