#!/usr/bin/env python3

import re
import nltk
import zhon.hanzi as hanzi

ENG_PUNCT = (';', ':', ',', '.', '!', '?', '\'')
LZH_PUNCT = hanzi.punctuation + '﹔'


class Language(object):
    @staticmethod
    def tokenize(string):
        raise NotImplementedError

    @staticmethod
    def stem(word_list, stemmer):
        raise NotImplementedError


class ClassicalChinese(Language):
    iso_code = 'lzh'

    @staticmethod
    def tokenize(string):
        return [character for character in string
                if character not in LZH_PUNCT]

    @staticmethod
    def split_sentences(string):
        return re.findall(hanzi.sentence, string)


class English(Language):
    iso_code = 'eng'

    @staticmethod
    def tokenize(string):
        tokens = nltk.tokenize.wordpunct_tokenize(string.lower())
        return [token for token in tokens
                if token not in ENG_PUNCT]

    @staticmethod
    def split_sentences(string):
        return nltk.sent_tokenize(string)

    # @staticmethod
    # def stem(word_list, stemmer=nltk.PorterStemmer()):
    #     return [stemmer.stem(word) for word in word_list]

