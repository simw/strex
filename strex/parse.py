
from __future__ import unicode_literals
from __future__ import absolute_import

from collections import Iterable, Mapping
from six import string_types

from strex.addins.basic_addins import ItemWare, ListWare
from strex.query_engines.xpath import XpathEngine
from strex.query_engines.regexp import RegexpEngine
from strex.query_engines.jsonpath import JsonEngine

# TODO: 
# 2) Convert XPath to compiled lxml expression
# 3) be more careful about unicode encoding for lxml (?)
# 4) be more careful with exceptions for corner cases:
#    a) xpath returns a list instead of a string
# 5) add named recursion
# 6) add option to ignore blanks (after stripping whitespace)
# 7) what happens if extract_structure returns an object?

default_query_engine_list = {
    'xpath': XpathEngine,
    'json': JsonEngine,
    'regexp': RegexpEngine
}

DEFAULT_QUERY_ENGINE = 'xpath'

default_wares_list = [
    ('_list', ListWare),
    ('_item', ItemWare)
]

class Parser(object):
    def __init__(self, options, query_engine=DEFAULT_QUERY_ENGINE):
        self.set_engine(query_engine, options)
        
        # Setup the default addins
        self.wares = []
        for (k, v) in default_wares_list:
            self.use(k, v, options)

    def set_engine(self, query_engine, options=None):
        self.engine = None
        if isinstance(query_engine, string_types):
            if query_engine not in default_query_engine_list: 
                raise Exception('Query Engine {0} does not exist'.format(query_engine))
            self.engine = default_query_engine_list[query_engine](options)

        else:
            # if not query_engine.get('get_doc') or not query_engine.get('run_query'):
            #     raise Exception('Query Engine object not understood')
            self.engine = query_engine(options)

    def use(self, tag, ware, options=None):
        this_ware = ware(tag, options)
        self.wares.append({
            'tag': tag,
            'ware': this_ware
        })

    def extract_structure(self, structure, doc):
        # if structure is a string, then pass to query engine
        if isinstance(structure, string_types): 
            return self.engine.run_query(structure, doc)

        # iterate through added processing options
        for ware in self.wares:
            if ware['tag'] in structure:
                return ware['ware'].run(self, structure, doc)

        # if structure is an iterable type, then recur
        if isinstance(structure, Iterable):
            if isinstance(structure, Mapping):
                # Is dictionary-like
                res = {}
                for k, v in structure.items():
                    res[k] = self.extract_structure(v, doc)
            else:
                # Is list-like
                res = []
                for v in structure:
                    res.append(self.extract_structure(v, doc))
            
            return res

        # all supported options are above and include a return statement
        # hence, if we get here then the structure hasn't been understood
        raise Exception('extract_structure: unknown type in structure tree ({0})\
            , should be string, dictionary or list'.format(type(structure)))

    def parse(self, structure, page, error_for_missing=False):
        if page:
            doc = self.engine.get_doc(page)
        else:
            doc = None
        return self.extract_structure(structure, doc)

