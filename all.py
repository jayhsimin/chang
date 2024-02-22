import os
import pandas as pd
from fuzzywuzzy import fuzz
import scipy.stats
import numpy as np
from scipy.spatial.distance import hamming
import Levenshtein
from glob import glob
import re
import statistics

# Dice coefficient distance
def bigram_sequence(text_lst):
    result = [a for ls in text_lst for a in zip(ls.split(",")[:-1], ls.split(",")[1:])]
    return result

# Jaccard Similarity
def jaccard_similarity(a, b):
    a = set(a)
    b = set(b)
    intersection = len(a.intersection(b))
    union = len(a.union(b))
    return intersection / union

# Dice coefficient distance
def dice(c, d):
    c = set(c)
    d = set(d)
    return (2 * len(c.intersection(d))) / (len(c) + len(d))

# Levenshtein Distance
def levenshtein_distance(a, b):
    ratio = Levenshtein.ratio(a, b)
    dist = Levenshtein.distance(a, b)
    return ratio, dist

# Hamming Distance
def hamming_distance(a, b):
    return hamming(a, b) * len(a)

# Wasserstein Distance
def wasserstein_distance(a, b):
    P = np.array(a)
    Q = np.array(b)
    dists = [i for i in range(len(P))]
    return scipy.stats.wasserstein_distance(dists, dists, P, Q)

# Zhang-style Wasserstein Distance
def wasserstein_distance_chang(a, b):
    c = tuple(abs(a[i] - b[i]) for i in range(len(a)))
    l = 0
    if range(len(c)) == range(0, 4):
        for discrepancy in c:
            if discrepancy in range(0, 1):
                l = l + discrepancy * 1
            if discrepancy in range(1, 3):
                l = l + discrepancy * 1
            if discrepancy in range(3, 5):
                l = l + discrepancy * 2
    if range(len(c)) == range(0, 8):
        for discrepancy in c:
            if discrepancy in range(0, 3):
                l = l + discrepancy * 2
            if discrepancy in range(3, 5):
                l = l + discrepancy * 2
            if discrepancy in range(5, 9):
                l = l + discrepancy * 3
    if range(len(c)) == range(0, 12):
        for discrepancy in c:
            if discrepancy in range(0, 4):
                l = l + discrepancy * 3
            if discrepancy in range(4, 8):
                l = l + discrepancy * 3
            if discrepancy in range(8, 12):
                l = l + discrepancy * 5
    return l

# Fuzzy String Matching
def fuzzy_string_matching(a, b):
    approximate_string_distance = fuzz.ratio(a, b)
    partial_ratio = fuzz.partial_ratio(a, b)
    return approximate_string_distance, partial_ratio

def process_file(file):
    CK = []
    DK = []
    ss = []
    tt = []
    L_ratio = []
    L_distance = []
    H_distance = []
    W_Distance = []
    W_Distance_Chang = []
    A_ratio = []
    A_partial_ratio = []
    D_distance = []

    df = pd.read_csv(file)

    for i in range(df.shape[0]):
        CC = re.findall(r"\d+", df['xai_rank'][i])
        DD = re.findall(r'\d+', df['t_rank'][i])
        CK.append(CC)
        DK.append(DD)
        basenamess = os.path.basename(file)
        bks = os.path.splitext(basenamess)[0]

    df['x'] = CK
    df['fc'] = DK

    for s in CK:
        results = list(map(int, s))
        ss.append(results)
    for t in DK:
        results = list(map(int, t))
        tt.append(results)
    df['xai'] = ss
    df['xai-thi'] = tt

    for n in range(df.shape[0]):
        GG = tuple(ss[n])
        GF = tuple(tt[n])

        # levenshteinDistance(分數越小越好)*
        ratio, dist = levenshtein_distance(GG, GF)
        L_ratio.append(ratio)
        L_distance.append(dist)

        # hamming_distance*
        hamming_dist = hamming_distance(GG, GF)
        H_distance.append(hamming_dist)

        # Wasserstein Distance*
        Wasserstein_Distance = wasserstein_distance(GG, GF)
        W_Distance.append(Wasserstein_Distance)

        # 張式Wasserstein Distance *
        W_Distance_Chang.append(wasserstein_distance_chang(GG, GF))

        # Approximate string distance
        app_str_distance, part_ratio = fuzzy_string_matching(GG, GF)
        A_ratio.append(app_str_distance)
        A_partial_ratio.append(part_ratio)

        # Dice coefficient distance
        c = bigram_sequence([str(GG)])
        d = bigram_sequence([str(GF)])
        Dice = dice(c, d)
        D_distance.append(Dice)

    df['L_ratio'] = L_ratio
    df['L_distance'] = L_distance
    df['H_distance'] = H_distance
    df['W_Distance'] = W_Distance
    df['W_Distance_Chang'] = W_Distance_Chang
    df['A_ratio'] = A_ratio
    df['A_partial_ratio'] = A_partial_ratio
    df['D_distance'] = D_distance

    aa = df.drop(columns=['xai_rank', 't_rank', 'x', 'fc'])
    aa.to_csv(f'{fin}/{bks}_a.csv', index=False)

cpath = r'C:\Users\vghuser\Desktop\xxx\all_s\divide\xai-thi'
fin = os.path.join(cpath, 'final')

if not os.path.isdir(fin):
    os.mkdir(fin)

file1 = glob(f'{cpath}/*.csv')
for file in file1:
    process_file(file)
