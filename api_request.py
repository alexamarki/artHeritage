from requests import get
import json


def basic_request(text_query):
    with open('out.json', 'r') as f:
        return json.load(f)


def configurated_request(text_query, params):
    pass


def info_get(link_query):
    pass

# url = 'http://sparql.europeana.eu/'
# query = """PREFIX dc: <http://purl.org/dc/elements/1.1/>
#     PREFIX edm: <http://www.europeana.eu/schemas/edm/>
#     PREFIX ore: <http://www.openarchives.org/ore/terms/>
#     SELECT ?title ?creator ?mediaURL ?date
#     WHERE {
#       ?CHO edm:type "IMAGE" ;
#           ore:proxyIn ?proxy;
#           dc:title ?title ;
#           dc:creator ?creator ;
#           dc:date ?date .
#       ?proxy edm:isShownBy ?mediaURL .
#     }
#     LIMIT 100
#     """
# # url = 'https://api.europeana.eu/record/v2/search.json'
# # query= 'Salvador Dali'
#
# r = get(url, params={'wskey': 'uckamage', 'format': 'json', 'query': query, 'theme': 'art'})
# data = r.json()
# with open('out.json', 'w') as outfile:
#     json.dump(data, outfile)
#
# # asynchronous programming???
