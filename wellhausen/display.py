#!/usr/bin/env python3

from io import StringIO
from mako.template import Template
from mako.runtime import Context
from mako.lookup import TemplateLookup


def render_html(corpus, cluster_assignments, filename):
    t = Template(filename="wellhausen/templates/html_out.mak")
    buf = StringIO()
    ctx = Context(buf,
                  corpus=corpus,
                  cluster_assignments=cluster_assignments)
    t.render_context(ctx)
    with open(filename, "w", encoding='utf-8') as f:
        f.write(buf.getvalue())