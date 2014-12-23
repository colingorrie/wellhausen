#!/usr/bin/env python3

import re

import pandas as pd
import zhon.hanzi as hanzi


HANZI_PUNCT = hanzi.punctuation + '﹔'


class Linguistic(object):
    def __init__(self, content=None):
        self.content = content

    def __str__(self):
        return str(self._flat_content)

    @property
    def characters(self):
        return [character for character in self._flat_content
                if character not in HANZI_PUNCT]

    @property
    def bag_of_words(self):
        char_set = set(self.characters)
        counts = dict()
        for char in char_set:
            counts[char] = self.characters.count(char)
        return pd.Series(counts)

    @property
    def _flat_content(self):
        return re.sub('\n', '', self.content)


class Sentence(Linguistic):
    pass


class Collection(Linguistic):
    @property
    def sentences(self):
        return re.findall(hanzi.sentence, self._flat_content)


class Text(Collection):
    def __str__(self):
        return '<div class="text">{}</div>'.format(''.join(str(section) for section in self.sections))

    @classmethod
    def from_file(cls, fn):
        with open(fn, encoding='utf-8') as f:
            return cls(f.read())

    @property
    def sections(self):
        split_lines = self.content.splitlines()
        return [Section(line) for line in split_lines]


class Section(Collection):
    def __str__(self):
        return '<div class="section">{}</div>'.format(self.content)
