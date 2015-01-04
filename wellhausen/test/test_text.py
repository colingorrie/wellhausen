#!/usr/bin/env python3

import os
import unittest

from wellhausen import text
from wellhausen import languages

DDJ_START = '道可道，非常道。名可名，非常名。無，名天地之始﹔有，名萬物之母。故常無，欲以觀其妙；常有，欲以觀其徼。此兩者，同出而異名，同謂之玄。玄之又玄，眾妙之門。\n天下皆知美之為美，斯惡矣﹔皆知善之為善，斯不善矣。故有無相生，難易相成，長短相形，高下相傾，音聲相和，前後相隨。是以聖人處「無為」之事，行「不言」之教。萬物作焉而不辭，生而不有，為而不恃，功成而弗居。夫唯弗居，是以不去。\n不尚賢，使民不爭﹔不貴難得之貨，使民不為盜﹔不見可欲，使民心不亂。是以「聖人」之治，虛其心，實其腹，弱其志，強其骨。常使民無知無欲。使夫智者不敢為也。為「無為」，則無不治。'
DDJ_3 = '不尚賢，使民不爭﹔不貴難得之貨，使民不為盜﹔不見可欲，使民心不亂。是以「聖人」之治，虛其心，實其腹，弱其志，強其骨。常使民無知無欲。使夫智者不敢為也。為「無為」，則無不治。'
THE_ROOM = "Oh man, I just can't figure women out. Sometimes they're just too smart. \nSometimes they're just flat-out stupid. Other times they're just evil."

class TextFromFileTest(unittest.TestCase):
    def setUp(self):
        self.text = text.Text.from_file(os.path.join(
            '..',
            '..',
            'data',
            'ddj.txt'
        ))

    def test_content_matches_constructor(self):
        self.assertTrue(self.text.content.startswith('道可道，非常道'))
        self.assertEqual('ddj.txt', self.text.title)
        self.assertEqual('lzh', self.text.language.iso_code)

    def test_sections(self):
        self.assertEqual(81, len(self.text.sections))

    def test_sentences(self):
        self.assertEqual(427, len(self.text.sentences))

    def test_words(self):
        self.assertEqual(5299, len(self.text.words))
        self.assertEqual('求', self.text.words[4905])

class TextFromStringTest(unittest.TestCase):
    def setUp(self):
        self.text = text.Text(DDJ_START, 'ddj_start')

    def test_content_matches_constructor(self):
        self.assertTrue(self.text.content.endswith('則無不治。'))
        self.assertEqual('ddj_start', self.text.title)

    def test_sections(self):
        self.assertEqual(3, len(self.text.sections))
        self.assertEqual(DDJ_3, self.text.sections[2].content)

    def test_sentences(self):
        self.assertEqual(16, len(self.text.sentences))
        self.assertEqual('為「無為」，則無不治。', self.text.sentences[15])

    def test_words(self):
        self.assertEqual(214, len(self.text.words))
        self.assertEqual('非', self.text.words[9])

    def test_bag_of_words(self):
        self.assertEqual(101, len(self.text.bag_of_words))
        self.assertEqual(3, self.text.bag_of_words['道'])


class SectionTest(unittest.TestCase):
    def setUp(self):
        self.section = text.Section('道可道，非常道。名可名，非常名。')

    def test_content_matches_constructor(self):
        self.assertEqual('道可道，非常道。名可名，非常名。', self.section.content)

    def test_string_reproduction(self):
        self.assertEqual('道可道，非常道。名可名，非常名。', str(self.section))

    def test_sentences(self):
        self.assertEqual(2, len(self.section.sentences))

    def test_words(self):
        self.assertEqual(12, len(self.section.words))
        self.assertEqual('名', self.section.words[8])

    def test_bag_of_words(self):
        self.assertEqual(5, len(self.section.bag_of_words))
        self.assertEqual(3, self.section.bag_of_words['道'])


class SentenceTest(unittest.TestCase):
    def setUp(self):
        self.section = text.Section('道可道，非常道。名可名，非常名。')

    def test_content_matches_constructor(self):
        self.assertEqual('道可道，非常道。名可名，非常名。', self.section.content)

    def test_string_reproduction(self):
        self.assertEqual('道可道，非常道。名可名，非常名。', str(self.section))

    def test_sentences(self):
        self.assertEqual(2, len(self.section.sentences))

    def test_words(self):
        self.assertEqual(12, len(self.section.words))
        self.assertEqual('名', self.section.words[8])

    def test_bag_of_words(self):
        self.assertEqual(5, len(self.section.bag_of_words))
        self.assertEqual(3, self.section.bag_of_words['道'])


class EnglishTextFromStringTest(unittest.TestCase):
    def setUp(self):
        self.text = text.Text(THE_ROOM, 'the_room', language=languages.English)

    def test_content_matches_constructor(self):
        self.assertTrue(self.text.content.endswith('evil.'))
        self.assertEqual('the_room', self.text.title)

    def test_sections(self):
        self.assertEqual(2, len(self.text.sections))
        self.assertEqual("Sometimes they're just flat-out stupid. Other times they're just evil.", self.text.sections[1].content)

    def test_sentences(self):
        self.assertEqual(4, len(self.text.sentences))
        self.assertEqual("Sometimes they're just flat-out stupid.", self.text.sentences[2])

    def test_words(self):
        self.assertEqual(29, len(self.text.words))
        self.assertEqual('sometimes', self.text.words[9])

    def test_bag_of_words(self):
        self.assertEqual(20, len(self.text.bag_of_words))
        self.assertEqual(4, self.text.bag_of_words['just'])


class EnglishSectionTest(unittest.TestCase):
    def setUp(self):
        self.section = text.Section(
            "Yeah, man, you'll never know. People are very strange these days.",
            language=languages.English,
        )

    def test_content_matches_constructor(self):
        self.assertEqual(
            "Yeah, man, you'll never know. People are very strange these days.",
            self.section.content
        )

    def test_string_reproduction(self):
        self.assertEqual(
            "Yeah, man, you'll never know. People are very strange these days.",
            str(self.section)
        )

    def test_sentences(self):
        self.assertEqual(2, len(self.section.sentences))

    def test_words(self):
        self.assertEqual(12, len(self.section.words))
        self.assertEqual('strange', self.section.words[9])

    def test_bag_of_words(self):
        self.assertEqual(12, len(self.section.bag_of_words))
        self.assertEqual(1, self.section.bag_of_words['you'])


class EnglishSentenceTest(unittest.TestCase):
    def setUp(self):
        self.sentence = text.Sentence('How good is good enough?', language=languages.English)

    def test_string_reproduction(self):
        self.assertEqual('How good is good enough?', str(self.sentence))

    def test_words(self):
        self.assertEqual(5, len(self.sentence.words))
        self.assertEqual('good', self.sentence.words[3])

    def test_bag_of_words(self):
        self.assertEqual(4, len(self.sentence.bag_of_words))
        self.assertEqual(2, self.sentence.bag_of_words['good'])
