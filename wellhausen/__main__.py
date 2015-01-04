#!/usr/bin/env python3

import os
from wellhausen import model
from wellhausen import corpus
from wellhausen import text
from wellhausen import display


def test():
    dao_de_jing = text.Text.from_file(os.path.join('..', 'data', 'ddj.txt'))
    lunyu = text.Text.from_file(os.path.join('..', 'data', 'lunyu.txt'))

    wenyan_corpus = corpus.Corpus(text_model=model.BinaryModel())

    wenyan_corpus.add_text(lunyu)
    wenyan_corpus.add_text(dao_de_jing)

    #print(wenyan_corpus.vector_space)
    clustering = wenyan_corpus.clustering(n_clusters=2)
    display.render_html(wenyan_corpus, clustering, 'output.html')


if __name__ == '__main__':
    test()
