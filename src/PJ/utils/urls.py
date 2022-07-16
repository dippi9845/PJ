from requests import get as get_request
from requests import Response
from urllib.parse import urlparse, ParseResult, parse_qsl

def url_request(url : str, params=None) -> Response:
    return get_request(url=url, params=params)

def url_parameters(url : str) -> dict:
    '''
    Returns a dict containing all parameters in a dict
    '''
    return dict(parse_qsl(urlparse(url).query))