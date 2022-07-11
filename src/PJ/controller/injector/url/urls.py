from requests import get as get_request
from requests import Response


def url_request(url : str, params=None) -> Response:
    return get_request(url=url, params=params)