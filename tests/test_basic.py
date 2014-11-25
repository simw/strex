from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest
from strex.parse import Parser

optsXmlXpath = {
    'parser': 'xml',
    'list_type': 'xpath'
}

optsXmlXpathAtom = {
    'parser': 'xml',
    'list_type': 'xpath',
    'namespaces': {
        'a': 'http://www.w3.org/2005/Atom'
    }
}

optsXmlCss = {
    'parser': 'xml',
    'list_type': 'css'
}

xml_struct1 = '//title/text()'
re_struct1 = '<title>(.*?)</title>'

xml_struct2 = {
    '_item': '//title/text()'
}
re_struct2 = {
    '_item': '<title>(.*?)</title>'
}

xml_struct3 = {
    '_list': '//element',
    '_item': 'text()'
}
re_struct3 = {
    '_list': '<element.*?>(.*)</element>',
    '_item': ''
}

xml_struct4 = {
    '_list': 'element',
    '_item': 'text()'
}

struct5 = 'a:title/text()'

@pytest.fixture()
def input1():
    with open('tests/input1.xml', 'r') as f:
        xml = f.read()
    return xml
        
@pytest.fixture()
def input2():
    with open('tests/input2.xml', 'r') as f:
        xml = f.read()
    return xml
 
@pytest.mark.usefixtures('input1')
class TestRegexpStrex:
    def test_basic(self, input1):
        st = Parser(None, 'regexp')
        res = st.parse(re_struct1, input1)
        assert(res == 'Title')

    def test_item(self, input1):
        st = Parser(None, 'regexp')
        res = st.parse(re_struct2, input1)
        assert(res == 'Title')

    def test_list(self, input1):
        st = Parser(None, 'regexp')
        print(input1)
        print(re_struct3)
        res = st.parse(re_struct3, input1)
        print(res)
        assert(res == ['Content 1', 'Content 2'])

@pytest.mark.usefixtures('input1')
class TestLxmlStrex:
    def test_basic(self, input1):
        st = Parser(optsXmlXpath)
        res = st.parse(xml_struct1, input1)
        assert(res == 'Title')

    def test_item(self, input1):
        st = Parser(optsXmlXpath)
        res = st.parse(xml_struct2, input1)
        assert(res == 'Title')

    def test_list(self, input1):
        st = Parser(optsXmlXpath)
        res = st.parse(xml_struct3, input1)
        assert(len(res) == 2)
        assert(res[0] == 'Content 1')
        assert(res[1] == 'Content 2')

    def test_css_list(self, input1):
        st = Parser(optsXmlCss)
        res = st.parse(xml_struct4, input1)
        assert(len(res) == 2)
        assert(res[0] == 'Content 1')
        assert(res[1] == 'Content 2')

@pytest.mark.usefixtures('input2')
class TestStrexWithNamespace:
    def test_basic(self, input2):
        st = Parser(optsXmlXpathAtom)
        res = st.parse(struct5, input2)
        assert(res == 'Feed Title')

    
