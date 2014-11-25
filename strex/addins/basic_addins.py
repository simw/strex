
from collections import Iterable
from six import string_types

def item_structure(self, structure, doc):
    return self.extract_structure(structure.get('_item'), doc)

def list_structure(self, structure, doc):
    opts = {}
    if self.engine.options.get('list_type'):
        opts['query_type'] = self.engine.options['list_type']
    subdocs = self.engine.run_query(structure.get('_list'), doc, opts)
 
    # If the query isn't set up correctly, then this might return a string
    # or something that's not Iterable 
    if isinstance(subdocs, string_types):
        subdocs = [subdocs]

    if not isinstance(subdocs, Iterable):
        raise Exception('Expression {0} produced a non-iterable result \
                ({1}) instead of a list of nodes'.format(structure.get('_list'), type(subdocs)))

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
        res.append(self.extract_structure(structure.get('_item'), subdoc))
    return res

