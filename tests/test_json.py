
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest
from strex.parse import Parser
from strex.query_engines.jsonpath import JsonEngine

doc1 = """
{
    "title": "This is a title",
    "body": {
        "element": "this element"
    },
    "mylist": [
        "element1",
        "element2",
        "element3"
    ]
}
"""

struct1 = 'title'
struct2 = 'body.element'
struct3 = {
    '_list': 'mylist',
    '_item': ''
}

class TestJsonStrex:
    def test_basic1(self):
        
        st = Parser(None, JsonEngine)
        res = st.parse(struct1, doc1)
        assert(res == 'This is a title')

    def test_basic2(self):
        st = Parser(None, JsonEngine)
        res = st.parse(struct2, doc1)
        assert(res == 'this element')

    def test_list(self):
        st = Parser(None, JsonEngine)
        res = st.parse(struct3, doc1)
        assert(res == ['element1', 'element2', 'element3'])

