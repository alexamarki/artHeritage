from requests import get
import json

parameters=[]
req = get(f"https://api.vam.ac.uk/v2/objects/search?{'&'.join(parameters)}")
object_data = req.json()
object_records = object_data["records"]
with open('out.json', 'w') as outfile:
    json.dump(object_records, outfile)
def basic_request(text_query):
    return dew_it([f'q={text_query}'])[0]


def configurated_request(text_query, params):
    pass

def info_get(id):
    return dew_it([f'kw_system_number={id}'])

def dew_it(parameters):
    req = get(f"https://api.vam.ac.uk/v2/objects/search?{'&'.join(parameters)}")
    object_data = req.json()
    object_records = object_data["records"]
    # with open('out.json', 'w') as outfile:
    #     json.dump(object_records, outfile)
    return object_records, object_data["info"]["record_count"]

# url = 'http://sparql.europeana.eu/'

# query = """PREFIX dc: <http://purl.org/dc/elements/1.1/>
#     PREFIX edm: <http://www.europeana.eu/schemas/edm/>
#     PREFIX ore: <http://www.openarchives.org/ore/terms/>
#     SELECT ?title ?creator ?mediaURL ?date
#     WHERE {
#     ?Aggregation edm:aggregatedCHO ?ProvidedCHO ;
#           edm:country "France" .
#       ?CHO edm:type "IMAGE" ;
#           ore:proxyIn ?proxy;
#           dc:title ?title ;
#           dc:creator ?creator ;
#           dc:date ?date .
#       ?proxy edm:isShownBy ?mediaURL .
#     }
#     LIMIT 50
#     """
#
# r = get(url, params={'wskey': 'uckamage', 'format': 'json', 'query': query})
# data = r.json()
# with open('out.json', 'w') as outfile:
#     json.dump(data, outfile)
#
#
