#!/usr/bin/env python3

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
from wellhausen import model


class Corpus(object):
    def __init__(self, min_occurrences=1, text_model=model.BagOfWordsModel()):
        self.min_occurrences = min_occurrences
        self.text_model = text_model
        self.vector_space = pd.DataFrame()
        self.texts = []

    @property
    def similarity_matrix(self):
        if self.vector_space.shape[0] > 0 and self.vector_space.shape[1] > 0:
            return 1 - pairwise_distances(self.vector_space.transpose(), metric='cosine')
        else:
            raise ValueError

    def add_text(self, text):
        # TODO: Add text labels by: pd.concat([vspace1, vspace2], keys=['text1', 'text2'])
        text_vector_space = pd.DataFrame()
        for i, section in enumerate(text.sections):
            text_vector_space[i] = self.text_model.fit(section.characters)
        text_vector_space = self._filter_vector_space(text_vector_space, self.min_occurrences)
        self.vector_space = pd.concat([self.vector_space, text_vector_space], axis=1)\
            .fillna(value=0).astype('int')
        self.texts.append(text)

    def cluster_membership(self, n_clusters):
        """
        Implements simple chapter clustering algorithm described in section 3 of Akiva and Koppel (2013).
        """
        if n_clusters >= self.vector_space.shape[1]:
            raise ValueError('Cannot ask for more clusters than there are items in the corpus.')
        model = KMeans(n_clusters=n_clusters)
        return model.fit_predict(self.similarity_matrix)

    @staticmethod
    def _filter_vector_space(vector_space, min_occurrences):
        return vector_space.loc[(vector_space.sum(axis=1) >= min_occurrences), ]
