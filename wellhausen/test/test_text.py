#!/usr/bin/env python3

import os
import unittest

from wellhausen import text


DDJ_START = '道可道，非常道。名可名，非常名。無，名天地之始﹔有，名萬物之母。故常無，欲以觀其妙；常有，欲以觀其徼。此兩者，同出而異名，同謂之玄。玄之又玄，眾妙之門。\n天下皆知美之為美，斯惡矣﹔皆知善之為善，斯不善矣。故有無相生，難易相成，長短相形，高下相傾，音聲相和，前後相隨。是以聖人處「無為」之事，行「不言」之教。萬物作焉而不辭，生而不有，為而不恃，功成而弗居。夫唯弗居，是以不去。\n不尚賢，使民不爭﹔不貴難得之貨，使民不為盜﹔不見可欲，使民心不亂。是以「聖人」之治，虛其心，實其腹，弱其志，強其骨。常使民無知無欲。使夫智者不敢為也。為「無為」，則無不治。'
DDJ_3 = '不尚賢，使民不爭﹔不貴難得之貨，使民不為盜﹔不見可欲，使民心不亂。是以「聖人」之治，虛其心，實其腹，弱其志，強其骨。常使民無知無欲。使夫智者不敢為也。為「無為」，則無不治。'


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

    def test_sections(self):
        self.assertEqual(81, len(self.text.sections))

    def test_sentences(self):
        self.assertEqual(427, len(self.text.sentences))

    def test_characters(self):
        self.assertEqual(5299, len(self.text.characters))
        self.assertEqual('求', self.text.characters[4905])


class TextFromStringTest(unittest.TestCase):
    def setUp(self):
        self.text = text.Text(DDJ_START)

    def test_content_matches_constructor(self):
        self.assertTrue(self.text.content.endswith('則無不治。'))

    def test_sections(self):
        self.assertEqual(3, len(self.text.sections))
        self.assertEqual(DDJ_3, self.text.sections[2].content)

    def test_sentences(self):
        self.assertEqual(16, len(self.text.sentences))
        self.assertEqual('為「無為」，則無不治。', self.text.sentences[15])

    def test_characters(self):
        self.assertEqual(214, len(self.text.characters))
        self.assertEqual('非', self.text.characters[9])

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

    def test_characters(self):
        self.assertEqual(12, len(self.section.characters))
        self.assertEqual('名', self.section.characters[8])

    def test_bag_of_words(self):
        self.assertEqual(5, len(self.section.bag_of_words))
        self.assertEqual(3, self.section.bag_of_words['道'])


class SentenceTest(unittest.TestCase):
    def setUp(self):
        self.sentence = text.Sentence('道可道，非常道。')

    def test_string_reproduction(self):
        self.assertEqual('道可道，非常道。', str(self.sentence))

    def test_characters(self):
        self.assertEqual(6, len(self.sentence.characters))
        self.assertEqual('非', self.sentence.characters[3])

    def test_bag_of_words(self):
        self.assertEqual(4, len(self.sentence.bag_of_words))
        self.assertEqual(3, self.sentence.bag_of_words['道'])
