
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest
from strex.parse import Parser
from strex.addins.httpget import httpget

doc1 = 'http://www.google.com'

struct1 = {
    '_httpget': {
        'options': {
            'parser': 'html',
        },
        'structure': {
            '_item': '//title/text()'
        }
    }
}

doc2 = """
http://www.google.com
http://www.bing.com
http://www.yahoo.com
"""

struct2 = {
    '_list': '(.+)\s',
    '_item': {
        '_httpget': {
            'options': {
                'parser': 'html'
            },
            'structure': {
                '_item': '//title/text()'
            }
        }
    }
}

class TestStrexHttpGet:
    def test_basic(self):
        st = Parser(None, 'regexp')
        st.use('_httpget', httpget, None)
        res = st.parse(struct1, doc1)
        assert(res == 'Google')

    def test_list(self):
        st = Parser(None, 'regexp')
        st.use('_httpget', httpget, None)
        res = st.parse(struct2, doc2)
        print(res)
        assert(res == ['Google', 'Bing', 'Yahoo'])

