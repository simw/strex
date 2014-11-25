
from collections import Iterable
from six import string_types

class ItemWare(object):
    def __init__(self, tag, options=None):
        self.set_tag(tag) 

    def set_tag(self, tag):
        self.tag = tag

    def run(self, parser, structure, doc):
        return parser.extract_structure(structure.get(self.tag), doc)


class ListWare(object):
    def __init__(self, tag, options=None):
        self.set_tag(tag) 
        if options and options.get('list_type'):
            self.list_type = options['list_type']
        else:
            self.list_type = None

    def set_tag(self, tag):
        self.tag = tag

    def run(self, parser, structure, doc):
        opts = {}
        if self.list_type:
            opts['query_type'] = self.list_type
        subdocs = parser.engine.run_query(structure.get(self.tag), doc, opts)
     
        # If the query isn't set up correctly, then this might return a string
        # or something that's not Iterable 
        if isinstance(subdocs, string_types):
            subdocs = [subdocs]

        if not isinstance(subdocs, Iterable):
            raise Exception('Expression {0} produced a non-iterable result \
                    ({1}) instead of a list of nodes'.format(structure.get(self.tag), type(subdocs)))

        # Default item tag is '_item', make sure it exists
        # It's then up to the engine what to do for default / blank query
        if not '_item' in structure: 
            structure['_item'] = '' 

        # Extract results
        res = []
        for subdoc in subdocs:
            # if isinstance(subdoc, basestring):
            #     raise Exception('Expression ' + structure.get('_list') + ' produced a string ' +
            #         ' as an element instead of a node: ' + subdoc)
            res.append(parser.extract_structure(structure.get('_item'), subdoc))
        return res

