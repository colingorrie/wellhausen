#!/usr/bin/env python3

import os
import random
import unittest

from wellhausen import text
from wellhausen import languages

DDJ_START = '道可道，非常道。名可名，非常名。無，名天地之始﹔有，名萬物之母。故常無，欲以觀其妙；常有，欲以觀其徼。此兩者，同出而異名，同謂之玄。玄之又玄，眾妙之門。\n天下皆知美之為美，斯惡矣﹔皆知善之為善，斯不善矣。故有無相生，難易相成，長短相形，高下相傾，音聲相和，前後相隨。是以聖人處「無為」之事，行「不言」之教。萬物作焉而不辭，生而不有，為而不恃，功成而弗居。夫唯弗居，是以不去。\n不尚賢，使民不爭﹔不貴難得之貨，使民不為盜﹔不見可欲，使民心不亂。是以「聖人」之治，虛其心，實其腹，弱其志，強其骨。常使民無知無欲。使夫智者不敢為也。為「無為」，則無不治。'
DDJ_END = '和大怨，必有餘怨﹔報怨以德，安可以為善？是以聖人執左契，而不責于人。有德司契，無德司徹。天道無親，常與善人。\n小國寡民。使有什伯之器而不用﹔使民重死而不遠徙。雖有舟輿，無所乘之，雖有甲兵，無所陳之。使民復結繩而用之。甘其食，美其服，安其居，樂其俗。鄰國相望，雞犬之聲相聞，民至老死，不相往來。\n信言不美，美言不信。善者不辯，辯者不善。知者不博，博者不知。聖人不積，既以為人己愈有，既以與人己愈多。天之道，利而不害﹔聖人之道，為而不爭。'
DDJ_3 = '不尚賢，使民不爭﹔不貴難得之貨，使民不為盜﹔不見可欲，使民心不亂。是以「聖人」之治，虛其心，實其腹，弱其志，強其骨。常使民無知無欲。使夫智者不敢為也。為「無為」，則無不治。'
THE_ROOM = "And she loves you too, as a person, as a human bean! If everyone love each other, the world would be a better place to live in. Let's go eat, huh? \nYou are lying! I never hit you! You are tearing me apart, Lisa!"


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


class CompositeTextTest(unittest.TestCase):
    def text_max_chunk_size_1(self):
        random.seed(99)
        text_a = text.Text(
            'Sentence A1. Sentence A2. Sentence A3.',
            'text_a',
            language=languages.English,
        )
        text_b = text.Text(
            'Sentence B1. Sentence B2. Sentence B3.',
            'text_b',
            language=languages.English,
        )
        text_c = text.Text.composite_of(text_a, text_b, 1)

        expected_sentences = ['Sentence A1.', 'Sentence B1.', 'Sentence A2.',
                              'Sentence B2.', 'Sentence A3.', 'Sentence B3.',
        ]
        for i, sentence in enumerate(expected_sentences):
            self.assertEqual(sentence, text_c.sentences[i])

    def test_max_chunk_size_2(self):
        random.seed(45)
        text_a = text.Text(
            'Sentence A1. Sentence A2. Sentence A3.',
            'text_a',
            language=languages.English,
        )
        text_b = text.Text(
            'Sentence B1. Sentence B2. Sentence B3.',
            'text_b',
            language=languages.English,
        )
        text_c = text.Text.composite_of(text_a, text_b, 2)

        expected_sentences = ['Sentence A1.', 'Sentence A2.', 'Sentence B1.',
                              'Sentence B2.', 'Sentence A3.', 'Sentence B3.',
                              ]
        for i, sentence in enumerate(expected_sentences):
            self.assertEqual(sentence, text_c.sentences[i])

    def test_multilingual_composite_text_raises_error(self):
        lzh_text = text.Text(DDJ_START, 'ddj_start', language=languages.ClassicalChinese)
        eng_text = text.Text(THE_ROOM, 'the_room', language=languages.English)
        with self.assertRaises(ValueError):
            multiling_text = text.Text.composite_of(lzh_text, eng_text, 1)


class EnglishTextFromStringTest(unittest.TestCase):
    def setUp(self):
        self.text = text.Text(THE_ROOM, 'the_room', language=languages.English)

    def test_content_matches_constructor(self):
        self.assertTrue(self.text.content.endswith('Lisa!'))
        self.assertEqual('the_room', self.text.title)

    def test_sections(self):
        self.assertEqual(2, len(self.text.sections))
        self.assertEqual("You are lying! I never hit you! You are tearing me apart, Lisa!", self.text.sections[1].content)

    def test_sentences(self):
        self.assertEqual(6, len(self.text.sentences))
        self.assertEqual("I never hit you!", self.text.sentences[3])

    def test_words(self):
        self.assertEqual(45, len(self.text.words))
        self.assertEqual('human', self.text.words[10])

    def test_bag_of_words(self):
        self.assertEqual(38, len(self.text.bag_of_words))
        self.assertEqual(4, self.text.bag_of_words['you'])


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
