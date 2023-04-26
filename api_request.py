from requests import get


def basic_request(text_query, page):
    return dew_it([text_query], page)[0]


def configurated_request(query, page):
    return dew_it(query.split('&'), page)[0]


def info_get(obj_id):
    return dew_it([f'kw_system_number={obj_id}'])


def dew_it(parameters, page=1):
    parameters.append(f'page={page}')
    req = get(f"https://api.vam.ac.uk/v2/objects/search?{'&'.join(parameters)}")
    if req:
        object_data = req.json()
        object_records = object_data["records"]
        return object_records, object_data["info"]["record_count"]
    else:
        return None, 0
