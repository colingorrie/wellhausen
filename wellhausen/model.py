#!/usr/bin/env python3

import pandas as pd


class TextModel(object):
    def __init__(self):
        pass

    def fit(self, characters):
        raise NotImplementedError


class BagOfWordsModel(TextModel):

    def fit(self, characters):
        char_set = set(characters)
        counts = dict()
        for char in char_set:
            counts[char] = characters.count(char)
        return pd.Series(counts)


class BinaryModel(TextModel):

    def fit(self, characters):
        char_set = set(characters)
        counts = dict()
        for char in char_set:
            if characters.count(char) > 0:
                counts[char] = 1
        return pd.Series(counts)