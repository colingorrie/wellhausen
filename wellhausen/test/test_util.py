#!/usr/bin/env python3

import unittest

from wellhausen import text
from wellhausen import util
from wellhausen import corpus


DDJ_START = '道可道，非常道。名可名，非常名。無，名天地之始﹔有，名萬物之母。故常無，欲以觀其妙；常有，欲以觀其徼。此兩者，同出而異名，同謂之玄。玄之又玄，眾妙之門。\n天下皆知美之為美，斯惡矣﹔皆知善之為善，斯不善矣。故有無相生，難易相成，長短相形，高下相傾，音聲相和，前後相隨。是以聖人處「無為」之事，行「不言」之教。萬物作焉而不辭，生而不有，為而不恃，功成而弗居。夫唯弗居，是以不去。\n不尚賢，使民不爭﹔不貴難得之貨，使民不為盜﹔不見可欲，使民心不亂。是以「聖人」之治，虛其心，實其腹，弱其志，強其骨。常使民無知無欲。使夫智者不敢為也。為「無為」，則無不治。'


class CosineSimilarityTest(unittest.TestCase):

    def setUp(self):
        self.corpus = corpus.Corpus(min_occurrences=2)
        self.corpus.add_text(text.Text(DDJ_START))

    def test_cosine_similarity(self):
        self.assertAlmostEqual(0.48,
                               util.cosine_similarity(
                                   self.corpus.vector_space[0],
                                   self.corpus.vector_space[1],
                               ),
                               delta=0.01)
