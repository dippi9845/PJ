from requests import get, post
from requests import Response
from urllib.parse import urlparse, parse_qsl, urljoin, urlencode
from abc import ABC

class Urls(ABC):

    @staticmethod
    def get_request(url : str, params=None) -> Response:
        '''
        Perform a get request
        '''
        return get(url=url, params=params)

    @staticmethod
    def post_request(url : str, params : dict=None) -> Response:
        '''
        Perform a get request
        '''
        return post(url=url, params=params)

    @staticmethod
    def url_parameters(url : str) -> dict:
        '''
        Returns a dict containing all parameters in a dict
        '''
        return dict(parse_qsl(urlparse(url).query))

    @staticmethod
    def remove_query(url : str) -> str:
        '''
        Remove the query part from given url
        '''
        return url.split("?")[0]

    @staticmethod
    def unparse_url(url: str, params : dict) -> str:
        '''
        Create an url by given parameters
        '''
        if url[-1] != "?":
            url = url + "?"
        
        return url + urlencode(params)
