from requests import get


def basic_request(text_query):
    return dew_it([text_query])[0]


def configurated_request(query):
    return dew_it(query.split('&'))[0]


def info_get(id):
    return dew_it([f'kw_system_number={id}'])


def dew_it(parameters):
    req = get(f"https://api.vam.ac.uk/v2/objects/search?{'&'.join(parameters)}")
    object_data = req.json()
    object_records = object_data["records"]
    return object_records, object_data["info"]["record_count"]
