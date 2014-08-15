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

