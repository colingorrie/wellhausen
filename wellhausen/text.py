#!/usr/bin/env python3

import os
import random
import re

import pandas as pd
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

    @classmethod
    def composite_of(cls, text1, text2, max_chunk_size):
        if text1.language.iso_code != text2.language.iso_code:
            raise ValueError("Texts must be written in the same language.")
        text1.content = cls._ensure_final_newline(text1.content)
        text2.content = cls._ensure_final_newline(text2.content)

        composite_sentences = []
        i, j = 0, 0
        while len(composite_sentences) < len(text1.sentences) + len(text2.sentences):
            chunk1, i = cls._draw_chunk_from_text(text1, i, max_chunk_size)
            composite_sentences.extend(chunk1)
            chunk2, j = cls._draw_chunk_from_text(text2, j, max_chunk_size)
            composite_sentences.extend(chunk2)

        return cls(
            ' '.join(composite_sentences),
            'Composite of {title1} and {title2}'.format(
                title1=text1.title,
                title2=text2.title,
            ),
            language=text1.language,
        )

    @property
    def sections(self):
        split_lines = self.content.splitlines()
        return [Section(line) for line in split_lines]

    @staticmethod
    def _ensure_final_newline(s):
        if s.endswith('\n'):
            return s
        else:
            return s + '\n'

    @staticmethod
    def _draw_chunk_from_text(t, i, max_chunk_size):
        chunk_size = random.randint(1, max_chunk_size)
        return t.sentences[i:i + chunk_size], i + chunk_size


class Section(Collection):
    def __str__(self):
        return self.content
