#!/usr/bin/env python3

import os
import re

import pandas as pd
import zhon.hanzi as hanzi
import wellhausen.languages as languages


class Linguistic(object):
    def __init__(self, content, language=languages.ClassicalChinese):
        self.content = content
        self.language = language

    def __str__(self):
        return str(self._flat_content)

    @property
    def words(self):
        return self.language.tokenize(self._flat_content)

    @property
    def bag_of_words(self):
        word_set = set(self.words)
        counts = dict()
        for word in word_set:
            counts[word] = self.words.count(word)
        return pd.Series(counts)

    @property
    def _flat_content(self):
        return re.sub('\n', '', self.content)


class Sentence(Linguistic):
    pass


class Collection(Linguistic):
    def __init__(self, content, language=languages.ClassicalChinese):
        super().__init__(content, language=language)

    @property
    def sentences(self):
        return self.language.split_sentences(self._flat_content)


class Text(Collection):
    def __init__(self, content, title, language=languages.ClassicalChinese):
        super().__init__(content, language)
        self.title = title

    @classmethod
    def from_file(cls, fn):
        with open(fn, encoding='utf-8') as f:
            return cls(f.read(), os.path.basename(fn))

    @property
    def sections(self):
        split_lines = self.content.splitlines()
        return [Section(line) for line in split_lines]


class Section(Collection):
    def __str__(self):
        return self.content
