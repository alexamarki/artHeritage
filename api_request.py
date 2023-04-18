from requests import get
import json

url = 'http://sparql.europeana.eu/'
query = """PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX edm: <http://www.europeana.eu/schemas/edm/>
PREFIX ore: <http://www.openarchives.org/ore/terms/>
SELECT ?title ?creator ?mediaURL ?date
WHERE {
  ?CHO edm:type "SOUND" ;
      ore:proxyIn ?proxy;
      dc:title ?title ;
      dc:creator ?creator ;
      dc:date ?date .
  ?proxy edm:isShownBy ?mediaURL .
}
LIMIT 100
"""
# url = 'https://api.europeana.eu/record/v2/search.json'
# query= 'Salvador Dali'

r = get(url, params={'wskey': 'uckamage', 'format': 'json', 'query': query})
data = r.json()
with open('out.json', 'w') as outfile:
    json.dump(data, outfile)

# asynchronous programming???

def basic_request(text_query):
    pass

def configurated_request(text_query, params):
    pass

def info_get(link_query):
    pass