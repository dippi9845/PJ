from requests import get as get_request
from requests import Response
from urllib.parse import urlparse, parse_qsl, urljoin

def url_request(url : str, params=None) -> Response:
    return get_request(url=url, params=params)

def url_parameters(url : str) -> dict:
    '''
    Returns a dict containing all parameters in a dict
    '''
    return dict(parse_qsl(urlparse(url).query))

def remove_query(url : str) -> str:
    return urljoin(url, urlparse(url).path)