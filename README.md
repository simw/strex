strex
=====

Python library for extracting structure from an html / xml page.

It uses lxml for the underlying parsing, and then uses xpath or css
selectors to turn that into a dictionary / object structure.

Examples
--------

'//title/text()'

{
  '_item': '//title/text()'
}

{
    'title': '//title/text()',
    'articles': {
        '_list': '//article/header/h1/a',
        '_item': {
            'name': 'text()',
            'link': '@href'
        }
    }
}

{
    '_name': 'element',
    '_item': {
        'element': 'name()',
        'attributes': {
            '_list': '@*',
            '_item': {
                'name': 'name()',
                'value': 'text()'
            }
        },
        'children': {
            '_list': 'child::node()',
            '_item': 'name()'
        }
    }
}

options = {
        'parser': 'html'
        'listtype': 'xpath' or 'css',
        'itemtype': 'xpath' or 'regexp',
        'namespaces': (optional) dictionary of xpath namespaces
    }
    
    eg0 single item
    structure = '//title'

    eg0.1 single item
    structure = {
        _item: '//title'
    }
    
    eg1 flat structure
    structure = {
        'link': 'a:id/text()',
        'published_date': 'a:published/text()'
    }

    eg2 flat structure - expanded
    structure = {
        'link': {
            '_item': 'a:id/text()'
        },
        'published_date': {
            '_item': 'a:published/text()'
        }
    }

    eg3 single list
    structure = {
        'links': {
            '_list': 'a',
            '_item': '@href'
        }
    }

    eg4 single list with substructure
    structure = {
        'sites': {
            '_list': 'a',
            '_item': {
                'url': '@href'
                'title': 'text()'
            }
        }
    }
