
import requests
from strex.parse import Parser

def httpget(self, structure, doc):
    obj = structure.get('_httpget') 

    if obj.get('url'):
        url = self.engine.run_query(obj['url'], doc)
    else:
        url = doc

    options = obj['options']
    structure = obj['structure']

    content = requests.get(url)
    st = Parser(options, 'xpath')
    res = st.parse(structure, content.text)
    return res 
