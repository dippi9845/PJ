from functools import partial
import unittest
from PJ.model.url import Url
from PJ.controller.injector.url_injector import UrlInjector
from PJ.utils.urls import Urls

class InjectorTests(unittest.TestCase):

    def check_by_list_of_combos(self, combos : list[str], url : str, params : dict):
        actual = Urls.unparse_url(url, params)
        self.assertIn(actual, combos)
        combos.remove(actual)

    def test_url_injector_inject_all(self):
        domain = "http://blablabla?k=null&j=null"
        payloads = ["1", "2", "3", "4", "5", "6"]
        
        url = Url(domain, vars_in_url_are_fixed=False)
        combinations = list(map(lambda x: domain.replace("null", x), payloads))
        to_call = partial(self.check_by_list_of_combos, combinations)

        injector = UrlInjector(url, payloads, request=to_call)
        injector.inject_all()
    
    def test_url_injector_by_iterator(self):
        domain = "http://blablabla?k=null&j=null"
        payloads = ["1", "2", "3", "4", "5", "6"]
        
        url = Url(domain, vars_in_url_are_fixed=False)
        combinations = list(map(lambda x: domain.replace("null", x), payloads))
        to_call = partial(self.check_by_list_of_combos, combinations)

        injector = UrlInjector(url, payloads, request=to_call)
        
        for _ in injector:
            pass
        
        self.assertListEqual(combinations, [])

if __name__ is "__main__":
    unittest.main()