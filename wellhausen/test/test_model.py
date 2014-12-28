#!/usr/bin/env python3

import unittest

from wellhausen import text
from wellhausen import model


DDJ_3 = '不尚賢，使民不爭﹔不貴難得之貨，使民不為盜﹔不見可欲，使民心不亂。是以「聖人」之治，虛其心，實其腹，弱其志，強其骨。常使民無知無欲。使夫智者不敢為也。為「無為」，則無不治。'


class BagOfWordsModelTest(unittest.TestCase):
    def setUp(self):
        self.ddj_3 = text.Text(DDJ_3, 'ddj_3')
        self.bow_model = model.BagOfWordsModel()

    def test_fit(self):
        self.assertEqual(40, len(self.bow_model.fit(self.ddj_3.characters)))
        self.assertEqual(8, self.bow_model.fit(self.ddj_3.characters)['不'])


class BinaryModelTest(unittest.TestCase):
    def setUp(self):
        self.ddj_3 = text.Text(DDJ_3, 'ddj_3')
        self.bin_model = model.BinaryModel()

    def test_fit(self):
        self.assertEqual(40, len(self.bin_model.fit(self.ddj_3.characters)))
        self.assertEqual(1, self.bin_model.fit(self.ddj_3.characters)['不'])
