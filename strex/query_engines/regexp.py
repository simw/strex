
from __future__ import unicode_literals

from collections import Iterable
from six import string_types
import re

default_options = {
    'remove_whitespace': True,
}

class RegexpEngine(object):
    def __init__(self, options):
        # Merge with default_options supplied above
        if options:
            default_options.update(options)
        options = default_options
        self.options = options

        self.remove_whitespace = options.get('remove_whitespace')

    def get_doc(self, page):
        doc = page
        return doc
       
    def run_query(self, query, doc, opts=None):
        if not query:
            return doc

        res = re.findall(query, doc)
        if not isinstance(res, string_types) and isinstance(res, Iterable):
            if len(res) == 1:
                res = res[0]
        if self.remove_whitespace:
            if isinstance(res, string_types):
                res = res.strip()
        return res

