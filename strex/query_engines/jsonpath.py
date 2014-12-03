
from __future__ import unicode_literals

import json
from six import string_types

class JsonEngine(object):
    def __init__(self, options=None):
        pass

    def get_doc(self, page):
        if isinstance(page, string_types):
            doc = json.loads(page)
        else:
            doc = page
        return doc

    def run_query(self, query, doc, opts=None):
        if query == '':
            return doc

        res = doc
        subqs = query.split('.')
        for q in subqs:
            tmp = q.split('[')
            key = tmp[0]
            index = None
            if len(tmp) > 1:
                index = int(tmp[1].strip(']'))
            res = res[key]
            if index != None:
                res = res[index]

        return res

