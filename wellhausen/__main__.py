#!/usr/bin/env python3

import os
from wellhausen import model
from wellhausen import corpus
from wellhausen import text
from wellhausen import display
from wellhausen import languages


def test():
    dao_de_jing = text.Text.from_file(os.path.join('..', 'data', 'ddj.txt'))
    lunyu = text.Text.from_file(os.path.join('..', 'data', 'lunyu.txt'))

    wenyan_corpus = corpus.Corpus(text_model=model.BinaryModel())

    wenyan_corpus.add_text(lunyu)
    wenyan_corpus.add_text(dao_de_jing)

    #print(wenyan_corpus.vector_space)
    clustering = wenyan_corpus.clustering(n_clusters=2)
    display.render_html(wenyan_corpus, clustering, 'output.html')


# def composite_test():
#     text_a = text.Text('Sentence A1. Sentence A2. Sentence A3.', 'text_a', language=languages.English)
#     text_b = text.Text('Sentence B1. Sentence B2. Sentence B3.', 'text_b', language=languages.English)
#     text_c = text.Text.composite_of(text_a, text_b, 4)
#     print(text_c.content)

if __name__ == '__main__':
    test()
    # composite_test()