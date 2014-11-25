
from __future__ import unicode_literals

from collections import Iterable, Mapping
from six import string_types

from strex.addins.basic_addins import item_structure, list_structure
from strex.query_engines.xpath import XpathEngine
from strex.query_engines.regexp import RegexpEngine

# TODO: 
# 2) Convert XPath to compiled lxml expression
# 3) be more careful about unicode encoding for lxml (?)
# 4) be more careful with exceptions for corner cases:
#    a) xpath returns a list instead of a string
# 5) add named recursion
# 6) add option to ignore blanks (after stripping whitespace)
# 7) what happens if extract_structure returns an object?

query_engines = {
    'xpath': XpathEngine,
    'regexp': RegexpEngine
}

class Parser(object):
    def __init__(self, options, query_engine='xpath'):
        # Set up the query engine
        self.engine = None
        if query_engine not in query_engines:
            raise Exception('Query Engine {0} does not exist'.format(query_engine))
        self.set_engine(query_engines[query_engine], options)
        
        # Setup the addins
        self.wares = []
        self.use('_list', list_structure, options)
        self.use('_item', item_structure, options)

    def set_engine(self, QueryEngine, options):
        self.engine = QueryEngine(options)

    def use(self, tag, fn, options):
        self.wares.append({
            'tag': tag,
            'fn': fn
        })

    def extract_structure(self, structure, doc):
        # if structure is a string, then pass to query engine
        if isinstance(structure, string_types): 
            return self.engine.run_query(structure, doc)

        # iterate through added processing options
        for ware in self.wares:
            if ware['tag'] in structure:
                return ware['fn'](self, structure, doc)

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

