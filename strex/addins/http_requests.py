
import requests
from strex.parse import Parser

class GetWare(object):
    def __init__(self, tag, options=None):
        self.set_tag(tag) 

    def set_tag(self, tag):
        self.tag = tag

    def run(self, parser, structure, doc):
        obj = structure.get('_httpget') 

        if obj.get('url'):
            url = parser.engine.run_query(obj['url'], doc)
        else:
            url = doc

        options = obj['options']
        structure = obj['structure']

        content = requests.get(url)
        st = Parser(options, 'xpath')
        res = st.parse(structure, content.text)
        return res 
