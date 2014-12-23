#!/usr/bin/env python3

import unittest

from wellhausen import corpus
from wellhausen import text
from wellhausen import model


DDJ_START = '道可道，非常道。名可名，非常名。無，名天地之始﹔有，名萬物之母。故常無，欲以觀其妙；常有，欲以觀其徼。此兩者，同出而異名，同謂之玄。玄之又玄，眾妙之門。\n天下皆知美之為美，斯惡矣﹔皆知善之為善，斯不善矣。故有無相生，難易相成，長短相形，高下相傾，音聲相和，前後相隨。是以聖人處「無為」之事，行「不言」之教。萬物作焉而不辭，生而不有，為而不恃，功成而弗居。夫唯弗居，是以不去。\n不尚賢，使民不爭﹔不貴難得之貨，使民不為盜﹔不見可欲，使民心不亂。是以「聖人」之治，虛其心，實其腹，弱其志，強其骨。常使民無知無欲。使夫智者不敢為也。為「無為」，則無不治。'
DDJ_END = '和大怨，必有餘怨﹔報怨以德，安可以為善？是以聖人執左契，而不責于人。有德司契，無德司徹。天道無親，常與善人。\n小國寡民。使有什伯之器而不用﹔使民重死而不遠徙。雖有舟輿，無所乘之，雖有甲兵，無所陳之。使民復結繩而用之。甘其食，美其服，安其居，樂其俗。鄰國相望，雞犬之聲相聞，民至老死，不相往來。\n信言不美，美言不信。善者不辯，辯者不善。知者不博，博者不知。聖人不積，既以為人己愈有，既以與人己愈多。天之道，利而不害﹔聖人之道，為而不爭。'


class CorpusWithImplicitBagOfWordsModelTest(unittest.TestCase):
    def setUp(self):
        self.corpus = corpus.Corpus()
        self.corpus.add_text(text.Text(DDJ_START))

    def test_string_reproduction(self):
        html_string = '<div class="text"><div class="section">道可道，非常道。名可名，非常名。無，名天地之始﹔有，名萬物之母。故常無，欲以觀其妙；常有，欲以觀其徼。此兩者，同出而異名，同謂之玄。玄之又玄，眾妙之門。</div><div class="section">天下皆知美之為美，斯惡矣﹔皆知善之為善，斯不善矣。故有無相生，難易相成，長短相形，高下相傾，音聲相和，前後相隨。是以聖人處「無為」之事，行「不言」之教。萬物作焉而不辭，生而不有，為而不恃，功成而弗居。夫唯弗居，是以不去。</div><div class="section">不尚賢，使民不爭﹔不貴難得之貨，使民不為盜﹔不見可欲，使民心不亂。是以「聖人」之治，虛其心，實其腹，弱其志，強其骨。常使民無知無欲。使夫智者不敢為也。為「無為」，則無不治。</div></div>'
        self.assertEqual(html_string, str(self.corpus))

    def test_from_text(self):
        self.assertEqual((33, 3), self.corpus.vector_space.shape)
        self.assertEqual(3, self.corpus.vector_space.loc['道', 0])
        self.assertEqual(1, len(self.corpus.texts))

    def test_similarity_matrix(self):
        self.assertEqual((3, 3), self.corpus.similarity_matrix.shape)
        self.assertAlmostEqual(0.48,
                               self.corpus.similarity_matrix[0, 2],
                               delta=0.01,
                               )


class CorpusWithBinaryTextModel(unittest.TestCase):
    def setUp(self):
        self.corpus = corpus.Corpus(text_model=model.BinaryModel())
        self.corpus.add_text(text.Text(DDJ_START))

    def test_binary_vector_space(self):
        self.assertEqual(1, self.corpus.vector_space.loc['道', 0])


class CorpusWithExplicitBagOfWordsModel(unittest.TestCase):
    def setUp(self):
        self.corpus = corpus.Corpus(text_model=model.BagOfWordsModel())
        self.corpus.add_text(text.Text(DDJ_START))

    def test_binary_vector_space(self):
        self.assertEqual(3, self.corpus.vector_space.loc['道', 0])


class EmptyCorpusTest(unittest.TestCase):
    def setUp(self):
        self.corpus = corpus.Corpus()

    def test_empty_texts_list(self):
        self.assertEqual(0, len(self.corpus.texts))

    def test_similarity_matrix(self):
        with self.assertRaises(ValueError):
            self.corpus.similarity_matrix()

    def test_clusters(self):
        with self.assertRaises(ValueError):
            self.corpus.cluster_membership(2)


class CorpusWithMultipleTextsTest(unittest.TestCase):
    def setUp(self):
        self.corpus = corpus.Corpus()
        self.corpus.add_text(text.Text(DDJ_START))
        self.corpus.add_text(text.Text(DDJ_END))

    def test_multiple_texts_are_appended(self):
        self.assertEqual((56, 6), self.corpus.vector_space.shape)
        self.assertEqual(2, len(self.corpus.texts))

    def test_cluster(self):
        self.assertEqual(6, len(self.corpus.cluster_membership(2)))


class CorpusWithCutoffValueTest(unittest.TestCase):
    def setUp(self):
        self.corpus = corpus.Corpus(min_occurrences=2)
        self.corpus.add_text(text.Text(DDJ_START))

    def test_from_text_with_cutoff(self):
        self.assertEqual((21, 3), self.corpus.vector_space.shape)

    def test_cluster(self):
        self.assertEqual(3, len(self.corpus.cluster_membership(2)))

    def test_cluster_with_more_clusters_than_individuals(self):
        with self.assertRaises(ValueError):
            self.corpus.cluster_membership(5)
