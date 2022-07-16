from requests import get as get_request
from requests import Response
from urllib.parse import urlparse, parse_qsl, urljoin, urlencode

def url_request(url : str, params=None) -> Response:
    '''
    Perform a get request
    '''
    return get_request(url=url, params=params)

def url_parameters(url : str) -> dict:
    '''
    Returns a dict containing all parameters in a dict
    '''
    return dict(parse_qsl(urlparse(url).query))

def remove_query(url : str) -> str:
    '''
    Remove the query part from given url
    '''
    return urljoin(url, urlparse(url).path)

def unparse_url(url: str, params : dict) -> str:
    '''
    Create an url by given parameters
    '''
    if url[-1] != "?":
        url = url + "?"
    
    return url + urlencode(params)
