#!/usr/bin/env python3

from wellhausen import model
from wellhausen import corpus
from wellhausen import text
from wellhausen import display


def test():
    dao_de_jing = text.Text.from_file('data\\ddj.txt')
    lunyu = text.Text.from_file('data\\lunyu.txt')

    wenyan_corpus = corpus.Corpus(text_model=model.BinaryModel())

    wenyan_corpus.add_text(lunyu)
    wenyan_corpus.add_text(dao_de_jing)

    #print(wenyan_corpus.vector_space)
    cluster_assignments = wenyan_corpus.cluster_membership(n_clusters=2)
    display.render_html(wenyan_corpus, cluster_assignments, "output.html")

if __name__ == '__main__':
    test()
