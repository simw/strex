strex
=====

Python library for extracting structure from unstructured data. 

For example:

    from Strex.parse import Parser

    doc = """
    Element 1
    Element 2
    Element 3
    """

    query_engine = 'regexp'

    structure = {
        '_list': '(.+)[\s]',
        '_item': ''
    }

    st = Parser(None, query_engine)
    print(st.parse(structure, doc))

will produce

    ['Element 1', 'Element 2', 'Element 3']

There are two implemented query engines:
1) regexp
2) xpath    

By default, it recognizes the list and item tags.

Examples
--------

Options:

    options = {
          'parser': 'html'
          'listtype': 'xpath' or 'css',
          'itemtype': 'xpath' or 'regexp',
          'namespaces': (optional) dictionary of xpath namespaces
      }

Stuctures:
      
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
