
from __future__ import unicode_literals

from collections import Iterable
from six import string_types

from lxml import etree, html
from cssselect import GenericTranslator

default_options = {
    'parser': 'html',
    'list_type': 'xpath',
    'item_type': 'xpath',
    'namespaces': None,
    'remove_whitespace': True,
    'absolute_links_base': False
}

class XpathEngine(object):
    def __init__(self, options=None):
        # Merge with default_options supplied above
        if options:
            default_options.update(options)
        options = default_options
        self.options = options

        self.parser = options['parser'].upper()
        if self.parser not in ['HTML', 'XML']:
            raise Excetpion('parser type unknown ({0}), should be XML or HTML'
                .format(self.parser))

        self.namespaces = options['namespaces']
        self.remove_whitespace = options.get('remove_whitespace')
        self.absolute_links_base = options['absolute_links_base']

    def get_doc(self, page):
        # Only pass utf-8 encoded string to lxml
        # In python2, it wants bytes not (unicode) string (?)
        page = page.encode('utf-8')
        if self.parser == 'HTML':
            doc = html.document_fromstring(page)
            if self.absolute_links_base:
                doc.make_links_absolute(self.absolute_links_base)

        elif self.parser == 'XML':
            doc = etree.fromstring(page)

        return doc

    def run_query(self, query, doc, opts=None):
        if not query:
            query = 'text()'

        if opts and opts.get('query_type'):
            if opts['query_type'] == 'css':
                query = GenericTranslator().css_to_xpath(query)

        res = doc.xpath(query, namespaces=self.namespaces)
        if not isinstance(res, string_types) and isinstance(res, Iterable):
            if len(res) == 1:
                res = res[0]
        
        if self.remove_whitespace:
            if isinstance(res, string_types):
                res = res.strip()
        return res

