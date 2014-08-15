from __future__ import unicode_literals

from lxml import etree, html
from cssselect import GenericTranslator

import collections

default_options = {
    'parser': 'html',
    'list_type': 'xpath',
    'item_type': 'xpath',
    'namespaces': None,
    'remove_whitespace': True
}

# TODO: 
# 1) Add regular expression parser
# 2) Convert XPath to compiled lxml expression
# 3) be more careful about unicode encoding for lxml (?)
# 4) be more careful with exceptions for corner cases:
#    a) xpath returns a list instead of a string
# 5) add named recursion
# 6) add option to ignore blanks (after stripping whitespace)


def extract_structure(doc, structure, options):

    # if structure is a string, then process
    if isinstance(structure, basestring):
        res = doc.xpath(structure, namespaces=options['namespaces'])
        if not isinstance(res, basestring):
            res = ' '.join(res)
        if options.get('remove_whitespace'):
            res = res.strip()
        return res
    
    # if structure has an attribute '_item', then process that
    if '_list' in structure: 
        res = []
        if not '_item' in structure: 
            structure['_item'] = 'text()' 

        if options['list_type'].lower() == 'xpath':
            xp = etree.XPath(structure.get('_list'), namespaces=options['namespaces'])           
            # subdocs = doc.xpath(structure.get('_list'), namespaces=options['namespaces'])
        elif options['list_type'].lower() == 'css':
            xp = etree.XPath(GenericTranslator().css_to_xpath(structure.get('_list')))
            # subdocs = doc.cssselect(structure.get('_list'))
        else:
            raise Exception('extract_structure: ' + options['list_type'] + ' not a valid ' +
                'list type')
        subdocs = xp(doc)

        # If the xpath isn't set up correclty, then this might return a string
        # instead of a list of nodes
        if isinstance(subdocs, basestring):
            raise Exception('Expression ' + structure.get('_list') + ' produced a string ' +
                ' instead of a list of nodes: ' + subdocs)

        for subdoc in subdocs:
            if isinstance(subdoc, basestring):
                raise Exception('Expression ' + structure.get('_list') + ' produced a string ' +
                    ' as an element instead of a node: ' + subdoc)
            res.append(extract_structure(subdoc, structure.get('_item'), options))
        return res

    # if object has an _item, then treat this as if it was simply a string
    # (having excluded the list possibility above)
    if '_item' in structure:
        return extract_structure(doc, structure.get('_item'), options)
        
    # if structure is some other type, then recur
    if isinstance(structure, collections.Iterable):
        if isinstance(structure, collections.Mapping):
            # Is dictionary-like
            res = {}
            for k, v in structure.items():
                res[k] = extract_structure(doc, v, options)
        else:
            # Is list-like
            res = []
            for v in structure:
                res.append(extract_structure(doc, v, options))
        
        return res


def parse(page, structure, options, absolute_links_base=None, error_for_missing=False):
    # Merge with default_options supplied above
    default_options.update(options)
    options = default_options

    # Only pass utf-8 encoded string to lxml
    # In python2, it wants bytes not (unicode) string
    if options['parser'].upper() == 'HTML':
        doc = html.document_fromstring(page.encode('utf-8'))
        if absolute_links_base:
            doc.make_links_absolute(absolute_links_base)
    elif options['parser'].upper() == 'XML':
        doc = etree.fromstring(page.encode('utf-8'))
    else:
        raise Exception('parse function: Unknown format for the page: ' + page_format)

    # Now, have an lxml object in doc - now convert to given structure
    return extract_structure(doc, structure, options)

