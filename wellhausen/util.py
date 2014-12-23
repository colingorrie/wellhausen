#!/usr/bin/env python3

import math


def cosine_similarity(vector1, vector2):
    # Courtesy http://stackoverflow.com/questions/18424228/cosine-similarity-between-2-number-lists
    sum_xx, sum_xy, sum_yy = 0, 0, 0
    for i in range(len(vector1)):
        x = vector1[i]
        y = vector2[i]
        sum_xx += x * x
        sum_yy += y * y
        sum_xy += x * y
    return sum_xy / math.sqrt(sum_xx*sum_yy)
