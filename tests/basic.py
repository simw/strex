import pytest
from strex.parse import parse

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

struct1 = '//title/text()'

struct2 = {
    '_list': '//element',
    '_item': 'text()'
}

struct3 = {
    '_list': 'element',
    '_item': 'text()'
}

struct4 = 'a:title/text()'

class TestStrex:
    def testBasic(self):
        xml = open('tests/input1.xml', 'r').read()
        res = parse(xml, struct1, optsXmlXpath)
        assert(res == 'Title')

    def testXpath(self):
        xml = open('tests/input1.xml', 'r').read()
        res = parse(xml, struct2, optsXmlXpath) 
        assert(len(res) == 2)
        assert(res[0] == 'Content 1')
        assert(res[1] == 'Content 2')

    def testCss(self):
        xml = open('tests/input1.xml', 'r').read()
        res = parse(xml, struct3, optsXmlCss) 
        assert(len(res) == 2)
        assert(res[0] == 'Content 1')
        assert(res[1] == 'Content 2')


class TestStrexWithNamespace:
    def testBasic(self):
        xml = open('tests/input2.xml', 'r').read()
        res = parse(xml, struct4, optsXmlXpathAtom)
        assert(res == 'Feed Title')

    
