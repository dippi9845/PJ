from functools import partial
import unittest
from PJ.controller.injector.injector import InjectorList
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
        
        url1 = Url(domain, vars_in_url_are_fixed=False)
        combinations = list(map(lambda x: domain.replace("null", x), payloads))
        to_call = partial(self.check_by_list_of_combos, combinations)

        injector = UrlInjector(url1, payloads, request=to_call)
        injector.inject_all()

        self.assertListEqual(combinations, [])
    
    def test_url_injector_by_iterator(self):
        domain = "http://blablabla?ada=null&kl=null"
        payloads = ["1", "2", "3", "4", "5", "6"]
        
        url2 = Url(domain, vars_in_url_are_fixed=False)
        combinations = list(map(lambda x: domain.replace("null", x), payloads))
        to_call = partial(self.check_by_list_of_combos, combinations)

        injector = UrlInjector(url2, payloads, request=to_call)
        
        for _ in injector:
            pass
        
        self.assertListEqual(combinations, [])
    
    def test_get_url(self):
        domain = "http://blablabla"
        params = "?giuseppino=null&francesco=null"
        url3 = Url(f"{domain}{params}")
        injector = UrlInjector(url3, [])

        self.assertEqual(injector.get_url(), url3.get_url())
        self.assertEqual(injector.get_url(), domain)

class InjectorListTests(unittest.TestCase):
    def check_by_list_of_combos(self, combos : list[str], url : str, params : dict):
        actual = Urls.unparse_url(url, params)
        self.assertIn(actual, combos)
        combos.remove(actual)

    def test_inject_all(self):
        domain1 = "http://blablabla?ada=null&kl=null"
        payloads1 = ["1", "2", "3", "4", "5", "6"]
        
        url1 = Url(domain1, vars_in_url_are_fixed=False)
        combinations1 = list(map(lambda x: domain1.replace("null", x), payloads1))
        to_call1 = partial(self.check_by_list_of_combos, combinations1)

        injector1 = UrlInjector(url1, payloads1, request=to_call1)

        domain2 = "http://ablaabla?dad=null&frenci=null"
        payloads2 = ["7", "8", "9", "10", "11", "12"]
        
        url2 = Url(domain2, vars_in_url_are_fixed=False)
        combinations2 = list(map(lambda x: domain2.replace("null", x), payloads2))
        to_call2 = partial(self.check_by_list_of_combos, combinations2)

        injector2 = UrlInjector(url2, payloads2, request=to_call2)

        injector = InjectorList([injector1, injector2])
        injector.inject_all()

        self.assertListEqual(combinations1, [])
        self.assertListEqual(combinations2, [])
    
    def test_iterator(self):
        domain1 = "http://blablabla?ada=null&kl=null"
        payloads1 = ["1", "2", "3", "4", "5", "6"]
        
        url1 = Url(domain1, vars_in_url_are_fixed=False)
        combinations1 = list(map(lambda x: domain1.replace("null", x), payloads1))
        to_call1 = partial(self.check_by_list_of_combos, combinations1)

        injector1 = UrlInjector(url1, payloads1, request=to_call1)

        domain2 = "http://ablaabla?dad=null&frenci=null"
        payloads2 = ["7", "8", "9", "10", "11", "12"]
        
        url2 = Url(domain2, vars_in_url_are_fixed=False)
        combinations2 = list(map(lambda x: domain2.replace("null", x), payloads2))
        to_call2 = partial(self.check_by_list_of_combos, combinations2)

        injector2 = UrlInjector(url2, payloads2, request=to_call2)

        injector = InjectorList([injector1, injector2])
        
        for i in injector:
            for j in i:
                pass

        self.assertListEqual(combinations1, [])
        self.assertListEqual(combinations2, [])
    
    def test_split(self):
        domain1 = "http://blablabla?ada=null&kl=null"
        payloads1 = ["1", "2", "3", "4", "5", "6"]
        
        url1 = Url(domain1, vars_in_url_are_fixed=False)
        combinations1 = list(map(lambda x: domain1.replace("null", x), payloads1))
        to_call1 = partial(self.check_by_list_of_combos, combinations1)

        injector1 = UrlInjector(url1, payloads1, request=to_call1)

        domain2 = "http://ablaabla?dad=null&frenci=null"
        payloads2 = ["7", "8", "9", "10", "11", "12"]
        
        url2 = Url(domain2, vars_in_url_are_fixed=False)
        combinations2 = list(map(lambda x: domain2.replace("null", x), payloads2))
        to_call2 = partial(self.check_by_list_of_combos, combinations2)

        injector2 = UrlInjector(url2, payloads2, request=to_call2)

        injector = InjectorList([injector1, injector2])

        injector = injector.split(2)

        self.assertIsInstance(injector[0], InjectorList)
        self.assertIsInstance(injector[1], InjectorList)
        
        self.assertIs(len(injector), 2)
        self.assertIs(len(injector[0]), 1)
        self.assertIs(len(injector[1]), 1)

        for i in injector:
            i.inject_all()
        
        self.assertListEqual(combinations1, [])
        self.assertListEqual(combinations2, [])
    
    def test_wrongs_split(self):
        domain1 = "http://blablabla?ada=null&kl=null"
        payloads1 = ["1", "2", "3", "4", "5", "6"]
        
        url1 = Url(domain1, vars_in_url_are_fixed=False)
        combinations1 = list(map(lambda x: domain1.replace("null", x), payloads1))
        to_call1 = partial(self.check_by_list_of_combos, combinations1)

        injector1 = UrlInjector(url1, payloads1, request=to_call1)

        domain2 = "http://ablaabla?dad=null&frenci=null"
        payloads2 = ["7", "8", "9", "10", "11", "12"]
        
        url2 = Url(domain2, vars_in_url_are_fixed=False)
        combinations2 = list(map(lambda x: domain2.replace("null", x), payloads2))
        to_call2 = partial(self.check_by_list_of_combos, combinations2)

        injector2 = UrlInjector(url2, payloads2, request=to_call2)

        injector = InjectorList([injector1, injector2])

        self.assertRaises(ValueError, injector.split, (3))

        self.assertRaises(ZeroDivisionError, injector.split, (0))




if __name__ is "__main__":
    unittest.main()