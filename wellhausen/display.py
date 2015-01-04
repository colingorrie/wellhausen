#!/usr/bin/env python3

from io import StringIO
import os
from mako.runtime import Context
from mako.lookup import TemplateLookup


mako_lookup = TemplateLookup(
    directories=[os.path.join('..', 'wellhausen', 'templates')],
    input_encoding='utf-8',
)

CLUSTER_NAMES = {0: 'one', 1: 'two', 2: 'three', 3: 'four', 4: 'five'}


def render_html(corpus, clustering, filename):
    t = mako_lookup.get_template('html_out.mak')
    buf = StringIO()
    ctx = Context(buf,
                  corpus=corpus,
                  clustering=clustering,
                  cluster_names=CLUSTER_NAMES,
                  )
    t.render_context(ctx)
    with open(filename, "w", encoding='utf-8') as f:
        f.write(buf.getvalue())
