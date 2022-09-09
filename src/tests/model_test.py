import unittest
from PJ.controller.injector.injector import InjectorList
from PJ.controller.injector.url_injector import UrlInjector
from PJ.model.variable import Variable, FixedVariable, InjectableVariable
from PJ.model.url import Url, ExportIdentifier as UrlExportIdentifier
from PJ.model.configuration import Configuration, ExportIdentifier as ConfigurationExportIdentifier, InjectionType

class TestUrl(unittest.TestCase):

    def test_gettes_default_fixed(self):
        domain = "https://domain"
        default_name = "default"
        default_value = "k"
        domani_p = domain + f"?{default_name}={default_value}"
        
        var1 = InjectableVariable("ciao", content="q")
        var2 = FixedVariable("hey", content="g")
        url1 = Url(domani_p, injectable_varaible=[var1], fixed_variable=[var2], vars_in_url_are_fixed=True)

        # test the removing of the parameters in the constructor
        self.assertEqual(url1.get_url(), domain, f"at the construction all the parameters need to be removed, {url1.get_url()} != {domain}")
        
        # test get_params()
        expected = {var1.get_variable_name() : var1.get_content(), var2.get_variable_name(): var2.get_content(), default_name : default_value}
        self.assertEqual(url1.get_params(), expected, f"Parameters are not the same. expected {expected} actual {url1.get_params()}")

        # test get_injectable_dict()
        expected = {var1.get_variable_name() : var1.get_content()}
        self.assertEqual(url1.get_injectable(), expected, f"injectable dict is not the same. Expected : {expected} actual {url1.get_injectable()}")
        
        # test get_fixed_dict()
        expected = {var2.get_variable_name() : var2.get_content(), default_name : default_value}
        self.assertEqual(url1.get_fixed(), expected, f"injectable dict is not the same. Expected : {expected} actual {url1.get_fixed()}")

    def test_gettes_default_injectable(self):
        domain = "https://domain"
        default_name = "default"
        default_value = "k"
        domani_p = domain + f"?{default_name}={default_value}"
        var1 = InjectableVariable("ciao", content="q")
        var2 = FixedVariable("hey", content="g")

        url2 = Url(domani_p, injectable_varaible=[var1], fixed_variable=[var2], vars_in_url_are_fixed=False)

        # test the removing of the parameters in the constructor
        self.assertEqual(url2.get_url(), domain, f"at the construction all the parameters need to be removed, {url2.get_url()} != {domain}")
        
        # test get_params()
        expected = {var1.get_variable_name() : var1.get_content(), var2.get_variable_name(): var2.get_content(), default_name : default_value}
        self.assertEqual(url2.get_params(), expected, f"Parameters are not the same. expected {expected} actual {url2.get_params()}")

        # test get_injectable_dict()
        expected = {var1.get_variable_name() : var1.get_content(), default_name : default_value}
        self.assertEqual(url2.get_injectable(), expected, f"injectable dict is not the same. Expected : {expected} actual {url2.get_injectable()}")
        
        # test get_fixed_dict()
        expected = {var2.get_variable_name() : var2.get_content()}
        self.assertEqual(url2.get_fixed(), expected, f"injectable dict is not the same. Expected : {expected} actual {url2.get_fixed()}")
    
    def test_gettes_default_ignored(self):
        domain = "https://domain"
        default_name = "default"
        default_value = "k"
        domani_p = domain + f"?{default_name}={default_value}"
        var1 = InjectableVariable("ciao", content="q")
        var2 = FixedVariable("hey", content="g")
        url3 = Url(domani_p, injectable_varaible=[var1], fixed_variable=[var2], vars_in_url_are_fixed=None)

        # test the removing of the parameters in the constructor
        self.assertEqual(url3.get_url(), domain, f"at the construction all the parameters need to be removed, {url3.get_url()} != {domain}")
        
        # test get_params()
        expected = {var1.get_variable_name() : var1.get_content(), var2.get_variable_name(): var2.get_content()}
        self.assertEqual(url3.get_params(), expected, f"Parameters are not the same. expected {expected} actual {url3.get_params()}")

        # test get_injectable_dict()
        expected = {var1.get_variable_name() : var1.get_content()}
        self.assertEqual(url3.get_injectable(), expected, f"injectable dict is not the same. Expected : {expected} actual {url3.get_injectable()}")
        
        # test get_fixed_dict()
        expected = {var2.get_variable_name() : var2.get_content()}
        self.assertEqual(url3.get_fixed(), expected, f"injectable dict is not the same. Expected : {expected} actual {url3.get_fixed()}")

    def test_to_dict(self):
        domain = "https://domain"
        default_name = "default"
        default_value = "k"
        domani_p = domain + f"?{default_name}={default_value}"
        var1 = InjectableVariable("ciao", content="q")
        var2 = FixedVariable("hey", content="g")
        url3 = Url(domani_p, injectable_varaible=[var1], fixed_variable=[var2], vars_in_url_are_fixed=None)

        expected = {
            UrlExportIdentifier.URL.value : domain,
            UrlExportIdentifier.INJECTABLE_VARAIBLE.value : {"ciao": "q"},
            UrlExportIdentifier.FIXED_VARAIBLE.value : {"hey": "g"}
        }

        self.assertDictEqual(expected, url3.to_dict())
    
    def test_from_dict(self):
        domain = "https://domain"
        
        expected = {
            UrlExportIdentifier.URL.value : domain,
            UrlExportIdentifier.INJECTABLE_VARAIBLE.value : {"ciao": "q"},
            UrlExportIdentifier.FIXED_VARAIBLE.value : {"hey": "g"}
        }

        url = Url.from_dict(expected)

        self.assertDictEqual(url.get_fixed(), {"hey": "g"})
        self.assertDictEqual(url.get_injectable(), {"ciao": "q"})
        self.assertEqual(url.get_url(), domain)
        self.assertEqual(url.get_params(), {"ciao": "q", "hey": "g"})

    
    def test_inject(self):
        domain = "https://domain"
        default_name = "default"
        default_value = "k"
        domani_p = domain + f"?{default_name}={default_value}"
        var1 = InjectableVariable("ciao", content="q")
        var2 = FixedVariable("hey", content="g")
        url3 = Url(domani_p, injectable_varaible=[var1], fixed_variable=[var2], vars_in_url_are_fixed=None)
        injected = url3.inject("babuino")

        self.assertEqual(injected, str(url3))

        possibility = [f"{domain}?ciao=babuino&hey=g", f"{domain}?hey=g&ciao=babuino"]

        self.assertIn(injected, possibility)

    
    def test_str(self):
        domain = "https://domain"
        default_name = "default"
        default_value = "k"
        domani_p = domain + f"?{default_name}={default_value}"
        var1 = InjectableVariable("ciao", content="q")
        var2 = FixedVariable("hey", content="g")
        url3 = Url(domani_p, injectable_varaible=[var1], fixed_variable=[var2], vars_in_url_are_fixed=None)

        possibilty = [f"{domain}?ciao=q&hey=g", f"{domain}?hey=g&ciao=q"]
        
        self.assertIn(str(url3), possibilty)
    
    def test_wrong_from_dict(self):
        domain = "https://domain"
        
        possible_dict = {
            UrlExportIdentifier.INJECTABLE_VARAIBLE.value : {"ciao": "q"},
            UrlExportIdentifier.FIXED_VARAIBLE.value : {"hey": "g"}
        }

        self.assertRaises(ValueError, Url.from_dict, (possible_dict))

        possible_dict_1 = {
            UrlExportIdentifier.URL.value : domain,
            UrlExportIdentifier.FIXED_VARAIBLE.value : {"hey": "g"}
        }

        self.assertRaises(ValueError, Url.from_dict, (possible_dict_1, False))

        possible_dict_2 = {
            UrlExportIdentifier.URL.value : domain,
            UrlExportIdentifier.INJECTABLE_VARAIBLE.value : {"ciao": "q"}
        }

        self.assertRaises(ValueError, Url.from_dict, (possible_dict_2, False))

        url1 = Url.from_dict(possible_dict_1)
        self.assertDictEqual(url1.get_injectable(), {})

        url2 = Url.from_dict(possible_dict_2)
        self.assertDictEqual(url2.get_fixed(), {})


class VaraibleTest(unittest.TestCase):
    
    VAR_NAME = "var name test"
    PROTOCOL = "PROTOCOL"
    CONTENT = "caio"

    def test_get_varaible(self):
        var = Variable(self.VAR_NAME)
        self.assertEqual(var.get_variable_name(), self.VAR_NAME, f"name should be {self.VAR_NAME}")

        var = Variable(self.VAR_NAME, protocol=self.PROTOCOL)
        self.assertEqual(var.get_protocol(), self.PROTOCOL,  f"protocol should be {self.PROTOCOL}")

        var = Variable(self.VAR_NAME, protocol=self.PROTOCOL, content=self.CONTENT)
        self.assertEqual(var.get_content(), self.CONTENT,  f"content should be {self.CONTENT}")

    def test_from_dict_single(self):
        var_dict = {self.VAR_NAME : self.CONTENT}
        var = Variable.from_dict(var_dict)

        self.assertEqual(var.get_variable_name(), self.VAR_NAME, f"name should be {self.VAR_NAME}")
        self.assertEqual(var.get_content(), self.CONTENT,  f"content should be {self.CONTENT}")
    
    def test_from_dict_multiple(self):
        second_name = "second name"
        second_content = "second content"

        var_dict = {self.VAR_NAME : self.CONTENT, second_name : second_content}
        var = Variable.from_dict(var_dict)

        self.assertEqual(type(var), list, "Should be a list")

        self.assertEqual(var[0].get_variable_name(), self.VAR_NAME, f"name should be {self.VAR_NAME}")
        self.assertEqual(var[0].get_content(), self.CONTENT,  f"content should be {self.CONTENT}")

        self.assertEqual(var[1].get_variable_name(), second_name, f"name should be {second_name}")
        self.assertEqual(var[1].get_content(), second_content,  f"content should be {second_content}")
    
    def test_to_dict(self):
        var = Variable(self.VAR_NAME, content=self.CONTENT)
        self.assertEqual(var.to_dict(), {self.VAR_NAME : self.CONTENT})

    def test_fixed(self):
        var = FixedVariable.from_variable(Variable(self.VAR_NAME, content=self.CONTENT))
        var.inject("bla bla")
        self.assertEqual(var.get_content(), self.CONTENT)


    def test_injectable(self):
        second_content = "content of test"
        empty = ""

        var = InjectableVariable.from_variable(Variable(self.VAR_NAME, content=self.CONTENT))
        var.inject(second_content)

        self.assertEqual(var.get_content(), second_content, f"Inject should set the content to: {second_content}")

        var.inject(empty)
        self.assertEqual(var.get_content(), empty, f"Inject should be able to set the content empty")


class ConfigurationTest(unittest.TestCase):
    RELATIVE_PATH = "src/tests/configrations/"
    
    def test_missing_version_fd(self):
        relative_path = self.RELATIVE_PATH + "no_version_config.json"
        fd = open(relative_path)
        self.assertRaises(ValueError, Configuration.from_file_descriptor, (fd))
    
    def test_missing_Injector_fd(self):
        relative_path = self.RELATIVE_PATH + "no_injector_config.json"
        fd = open(relative_path)
        self.assertRaises(ValueError, Configuration.from_file_descriptor, (fd))
    
    def test_missing_name_fd(self):
        relative_path = self.RELATIVE_PATH + "no_name_config.json"
        fd = open(relative_path)
        cnf = Configuration.from_file_descriptor(fd)
        self.assertEqual(cnf.config_name, "no_name_config.json")
    
    def test_missing_global_payloads_fd(self):
        relative_path = self.RELATIVE_PATH + "no_global_payloads.json"
        fd = open(relative_path)
        cnf = Configuration.from_file_descriptor(fd)
        self.assertEqual(Configuration.get_empty_payload_dict(), cnf.global_payloads)
    
    def test_missing_global_payloads_file_fd(self):
        relative_path = self.RELATIVE_PATH + "no_global_payloads_file.json"
        fd = open(relative_path)
        cnf = Configuration.from_file_descriptor(fd)
        self.assertEqual(Configuration.get_empty_payload_dict(type=list), cnf.global_payload_files)
        
    def test_missing_global_payloads_file_separetor_fd(self):
        relative_path = self.RELATIVE_PATH + "no_global_payload_file separetor.json"
        fd = open(relative_path)
        cnf = Configuration.from_file_descriptor(fd)
        self.assertEqual("\n", cnf.payload_file_separetor)
    
    def test_missing_version_fn(self):
        relative_path = self.RELATIVE_PATH + "no_version_config.json"
        self.assertRaises(ValueError, Configuration.from_file, (relative_path))
    
    def test_missing_Injector_fn(self):
        relative_path = self.RELATIVE_PATH + "no_injector_config.json"
        self.assertRaises(ValueError, Configuration.from_file, (relative_path))
    
    def test_missing_name_fn(self):
        relative_path = self.RELATIVE_PATH + "no_name_config.json"
        cnf = Configuration.from_file(relative_path)
        self.assertEqual(cnf.config_name, "no_name_config.json")
    
    def test_missing_global_payloads_fn(self):
        relative_path = self.RELATIVE_PATH + "no_global_payloads.json"
        cnf = Configuration.from_file(relative_path)
        self.assertEqual(Configuration.get_empty_payload_dict(), cnf.global_payloads)
    
    def test_missing_global_payloads_file_fn(self):
        relative_path = self.RELATIVE_PATH + "no_global_payloads_file.json"
        cnf = Configuration.from_file(relative_path)
        self.assertEqual(Configuration.get_empty_payload_dict(type=list), cnf.global_payload_files)
        
    def test_missing_global_payloads_file_separetor_fn(self):
        relative_path = self.RELATIVE_PATH + "no_global_payload_file separetor.json"
        cnf = Configuration.from_file(relative_path)
        self.assertEqual("\n", cnf.payload_file_separetor)
    
    def test_add_payload_file_by_key_list(self):
        to_add = [self.RELATIVE_PATH + "to_add1.txt", self.RELATIVE_PATH + "to_add2.txt"]
        
        expected = {
            InjectionType.URL.value: to_add,
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config")
        cnf.add_payload_file_by_key(InjectionType.URL.value, to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            cnf.global_payload_files[key].sort()
        
            self.assertListEqual(cnf.global_payload_files[key], expected[key])
        
        initial_list = [self.RELATIVE_PATH + "initial1.txt", self.RELATIVE_PATH + "initial2.txt"]
        
        initial = {
            InjectionType.URL.value: initial_list,
            InjectionType.WEBDRIVER.value : []
        }
        
        expected = {
            InjectionType.URL.value: initial_list + to_add,
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config", global_payload_files=initial)
        cnf.add_payload_file_by_key(InjectionType.URL.value, to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            cnf.global_payload_files[key].sort()
        
            self.assertListEqual(cnf.global_payload_files[key], expected[key])

    def test_add_payload_file_by_key_set(self):
        to_add = {self.RELATIVE_PATH + "to_add1.txt", self.RELATIVE_PATH + "to_add2.txt"}
        
        expected = {
            InjectionType.URL.value: list(to_add),
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config")
        cnf.add_payload_file_by_key(InjectionType.URL.value, to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            cnf.global_payload_files[key].sort()
        
            self.assertListEqual(cnf.global_payload_files[key], expected[key])
        
        initial_list = [self.RELATIVE_PATH + "initial1.txt", self.RELATIVE_PATH + "initial2.txt"]
        
        initial = {
            InjectionType.URL.value: initial_list,
            InjectionType.WEBDRIVER.value : []
        }
        
        expected = {
            InjectionType.URL.value: initial_list + list(to_add),
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config", global_payload_files=initial)
        cnf.add_payload_file_by_key(InjectionType.URL.value, to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            cnf.global_payload_files[key].sort()
        
            self.assertListEqual(cnf.global_payload_files[key], expected[key])
    
    def test_add_payload_file_by_key_single(self):
        to_add = self.RELATIVE_PATH + "to_add1.txt"
        
        expected = {
            InjectionType.URL.value: [to_add],
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config")
        cnf.add_payload_file_by_key(InjectionType.URL.value, to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            cnf.global_payload_files[key].sort()
        
            self.assertListEqual(cnf.global_payload_files[key], expected[key])
        
        initial_list = [self.RELATIVE_PATH + "initial1.txt", self.RELATIVE_PATH + "initial2.txt"]
        
        initial = {
            InjectionType.URL.value: initial_list,
            InjectionType.WEBDRIVER.value : []
        }
        
        expected = {
            InjectionType.URL.value: initial_list + [to_add],
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config", global_payload_files=initial)
        cnf.add_payload_file_by_key(InjectionType.URL.value, to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            cnf.global_payload_files[key].sort()
        
            self.assertListEqual(cnf.global_payload_files[key], expected[key])
    
    def test_add_payload_file_by_key_single_duplicate(self):
        to_add = self.RELATIVE_PATH + "initial1.txt"
        
        initial_list = [self.RELATIVE_PATH + "initial1.txt", self.RELATIVE_PATH + "initial2.txt"]
        
        initial = {
            InjectionType.URL.value: initial_list,
            InjectionType.WEBDRIVER.value : []
        }
        
        expected = {
            InjectionType.URL.value: initial_list,
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config", global_payload_files=initial)
        cnf.add_payload_file_by_key(InjectionType.URL.value, to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            cnf.global_payload_files[key].sort()
        
            self.assertListEqual(cnf.global_payload_files[key], expected[key])
    
    def test_add_payload_file_by_key_list_duplicate(self):
        to_add = [self.RELATIVE_PATH + "initial1.txt", self.RELATIVE_PATH + "initial2.txt"]
        
        initial_list = [self.RELATIVE_PATH + "initial1.txt", self.RELATIVE_PATH + "initial2.txt"]
        
        initial = {
            InjectionType.URL.value: initial_list,
            InjectionType.WEBDRIVER.value : []
        }
        
        expected = {
            InjectionType.URL.value: initial_list,
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config", global_payload_files=initial)
        cnf.add_payload_file_by_key(InjectionType.URL.value, to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            cnf.global_payload_files[key].sort()
        
            self.assertListEqual(cnf.global_payload_files[key], expected[key])

    def test_add_payload_file_by_dict_list(self):
        list_to_add = [self.RELATIVE_PATH + "to_add1.txt", self.RELATIVE_PATH + "to_add2.txt"]
        
        to_add = {
            InjectionType.URL.value: list_to_add,
            InjectionType.WEBDRIVER.value : []
        }
        
        expected = {
            InjectionType.URL.value: list_to_add,
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config")
        cnf.add_payload_file_by_dict(to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            cnf.global_payload_files[key].sort()
        
            self.assertListEqual(cnf.global_payload_files[key], expected[key])
        
        initial_list = [self.RELATIVE_PATH + "initial1.txt", self.RELATIVE_PATH + "initial2.txt"]
        
        initial = {
            InjectionType.URL.value: initial_list,
            InjectionType.WEBDRIVER.value : []
        }
        
        expected = {
            InjectionType.URL.value: initial_list + list_to_add,
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config", global_payload_files=initial)
        cnf.add_payload_file_by_dict(to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            cnf.global_payload_files[key].sort()
        
            self.assertListEqual(cnf.global_payload_files[key], expected[key])

    def test_add_payload_file_by_dict_set(self):
        set_to_add = {self.RELATIVE_PATH + "to_add1.txt", self.RELATIVE_PATH + "to_add2.txt"}
        
        to_add = {
            InjectionType.URL.value: set_to_add,
            InjectionType.WEBDRIVER.value : []
        }
        
        expected = {
            InjectionType.URL.value: list(set_to_add),
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config")
        cnf.add_payload_file_by_dict(to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            cnf.global_payload_files[key].sort()
        
            self.assertListEqual(cnf.global_payload_files[key], expected[key])
        
        initial_list = [self.RELATIVE_PATH + "initial1.txt", self.RELATIVE_PATH + "initial2.txt"]
        
        initial = {
            InjectionType.URL.value: initial_list,
            InjectionType.WEBDRIVER.value : []
        }
        
        expected = {
            InjectionType.URL.value: initial_list + list(set_to_add),
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config", global_payload_files=initial)
        cnf.add_payload_file_by_dict(to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            cnf.global_payload_files[key].sort()
        
            self.assertListEqual(cnf.global_payload_files[key], expected[key])
    
    def test_add_payload_file_by_dict_single(self):
        single_to_add = self.RELATIVE_PATH + "to_add1.txt"
        
        to_add = {
            InjectionType.URL.value: single_to_add,
            InjectionType.WEBDRIVER.value : []
        }
        
        expected = {
            InjectionType.URL.value: [single_to_add],
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config")
        cnf.add_payload_file_by_dict(to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            cnf.global_payload_files[key].sort()
        
            self.assertListEqual(cnf.global_payload_files[key], expected[key])
        
        initial_list = [self.RELATIVE_PATH + "initial1.txt", self.RELATIVE_PATH + "initial2.txt"]
        
        initial = {
            InjectionType.URL.value: initial_list,
            InjectionType.WEBDRIVER.value : []
        }
        
        expected = {
            InjectionType.URL.value: initial_list + [single_to_add],
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config", global_payload_files=initial)
        cnf.add_payload_file_by_dict(to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            cnf.global_payload_files[key].sort()
        
            self.assertListEqual(cnf.global_payload_files[key], expected[key])
    
    def test_add_payload_file_by_dict_single_duplicate(self):
        single_to_add = self.RELATIVE_PATH + "initial1.txt"
        
        to_add = {
            InjectionType.URL.value: single_to_add,
            InjectionType.WEBDRIVER.value : []
        }
        
        initial_list = [self.RELATIVE_PATH + "initial1.txt", self.RELATIVE_PATH + "initial2.txt"]
        
        initial = {
            InjectionType.URL.value: initial_list,
            InjectionType.WEBDRIVER.value : []
        }
        
        expected = {
            InjectionType.URL.value: initial_list,
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config", global_payload_files=initial)
        cnf.add_payload_file_by_dict(to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            cnf.global_payload_files[key].sort()
        
            self.assertListEqual(cnf.global_payload_files[key], expected[key])
    
    def test_add_payload_file_by_key_dict_duplicate(self):
        list_to_add = [self.RELATIVE_PATH + "initial1.txt", self.RELATIVE_PATH + "initial2.txt"]
        
        to_add = {
            InjectionType.URL.value: list_to_add,
            InjectionType.WEBDRIVER.value : []
        }
        
        initial_list = [self.RELATIVE_PATH + "initial1.txt", self.RELATIVE_PATH + "initial2.txt"]
        
        initial = {
            InjectionType.URL.value: initial_list,
            InjectionType.WEBDRIVER.value : []
        }
        
        expected = {
            InjectionType.URL.value: initial_list,
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config", global_payload_files=initial)
        cnf.add_payload_file_by_key(InjectionType.URL.value, to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            cnf.global_payload_files[key].sort()
        
            self.assertListEqual(cnf.global_payload_files[key], expected[key])
    
    def test_load_payload_file(self):
        to_add = self.RELATIVE_PATH + "to_add1.txt"
        
        with open(to_add, "r") as f:
            payloads = f.read().split("\n")
        
        expected = {
            InjectionType.URL.value: payloads,
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config")
        cnf.add_payload_file_by_key(InjectionType.URL.value, to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            actual = list(cnf.global_payloads[key])
            actual.sort()
        
            self.assertListEqual(actual, expected[key])
        
        initial_list = [self.RELATIVE_PATH + "initial1.txt", self.RELATIVE_PATH + "initial2.txt"]
        
        initial = {
            InjectionType.URL.value: initial_list,
            InjectionType.WEBDRIVER.value : []
        }
        
        files = initial_list + [to_add]
        payloads = []
        
        for i in files:
            with open(i, "r") as f:
                payloads += f.read().split("\n")
        
        expected = {
            InjectionType.URL.value: payloads,
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config", global_payload_files=initial)
        cnf.add_payload_file_by_key(InjectionType.URL.value, to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            actual = list(cnf.global_payloads[key])
            actual.sort()
        
            self.assertListEqual(actual, expected[key])
    
    def test_load_payload_file_duplicated(self):
        to_add = self.RELATIVE_PATH + "to_add1.txt"
        
        initial_list = [self.RELATIVE_PATH + "initial1.txt", self.RELATIVE_PATH + "initial2.txt"]
        
        initial = {
            InjectionType.URL.value: initial_list,
            InjectionType.WEBDRIVER.value : []
        }
        
        files = initial_list + [to_add]
        payloads = []
        
        for i in files:
            with open(i, "r") as f:
                payloads += f.read().split("\n")
        
        expected = {
            InjectionType.URL.value: payloads,
            InjectionType.WEBDRIVER.value : []
        }
        
        initail_payloads = {
            InjectionType.URL.value: ["initial1_4", "to_add1_4"],
            InjectionType.WEBDRIVER.value : []
        }
        
        cnf = Configuration(config_name="test add payload file by key config", global_payloads=initail_payloads, global_payload_files=initial)
        cnf.add_payload_file_by_key(InjectionType.URL.value, to_add)
        cnf.load_payload_file()
        
        for key in expected.keys():
            expected[key].sort()
            actual = list(cnf.global_payloads[key])
            actual.sort()
        
            self.assertListEqual(actual, expected[key])
        
    def test_serialize_injector(self):
        url_str = "https://sjdahfbakhs"
        
        expected = {
            ConfigurationExportIdentifier.INJECTOR_TYPE.value : InjectionType.URL.value
        }
        
        url1 = UrlInjector(Url(url_str), [])

        expected.update(url1.to_dict())
        
        self.assertDictEqual(Configuration.serialize_injector(url1), expected)
    
    def test_add_injector(self):
        url_str1 = "https://sjdahfbakhs"
        url_str2 = "https://sjdahfsdafasdfbakhs"
        
        url1 = UrlInjector(Url(url_str1), [])
        url2 = UrlInjector(Url(url_str2), [])
        
        expected = [
            {
                ConfigurationExportIdentifier.INJECTOR_TYPE.value : InjectionType.URL.value
            },
            {
                ConfigurationExportIdentifier.INJECTOR_TYPE.value : InjectionType.URL.value
            }
        ]
        expected[0].update(Configuration.serialize_injector(url1))
        expected[1].update(Configuration.serialize_injector(url2))
        
        cnf = Configuration(injector_list=InjectorList([url1]))
        cnf.add_injector(url2)
        
        self.assertListEqual(cnf.injectors_serialized, expected)
    
    def test_export_configuration_one_injector(self):
        url_str1 = "https://sjdahfbakhs"
        url1 = UrlInjector(Url(url_str1), [])
        to_add = [self.RELATIVE_PATH + "to_add1.txt", self.RELATIVE_PATH + "to_add2.txt"]
        payloads = []
        
        for i in to_add:
            with open(i, "r") as f:
                payloads += f.read().split("\n")
                
        cnf = Configuration(injector_list=InjectorList([url1]))
        cnf.add_payload_file_by_key(InjectionType.URL.value, to_add)
        cnf.load_payload_file()
        
        expected = {
            ConfigurationExportIdentifier.VERSION.value : cnf.config_version,
            ConfigurationExportIdentifier.CONFIGURATION_NAME.value : cnf.config_name,
            ConfigurationExportIdentifier.GLOBAL_PAYLOADS.value : {
                InjectionType.URL.value : payloads,
                InjectionType.WEBDRIVER.value : []
            },
            ConfigurationExportIdentifier.GLOBAL_PAYLOAD_FILES.value : {
                InjectionType.URL.value : to_add,
                InjectionType.WEBDRIVER.value : []
            },
            ConfigurationExportIdentifier.GLOBAL_PAYLOAD_FILE_SEPARETOR.value : cnf.payload_file_separetor,
            ConfigurationExportIdentifier.INJECTORS.value : cnf.injectors_serialized
        }
        actual = cnf.to_dict()
        self.maxDiff = None
        self.assertEqual(expected[ConfigurationExportIdentifier.VERSION.value], actual[ConfigurationExportIdentifier.VERSION.value])
        self.assertEqual(expected[ConfigurationExportIdentifier.CONFIGURATION_NAME.value], actual[ConfigurationExportIdentifier.CONFIGURATION_NAME.value])
        
        expected[ConfigurationExportIdentifier.GLOBAL_PAYLOADS.value][InjectionType.URL.value].sort()
        #expected[ConfigurationExportIdentifier.GLOBAL_PAYLOADS.value][InjectionType.URL.value].pop(0) # this element can't be here
        actual[ConfigurationExportIdentifier.GLOBAL_PAYLOADS.value][InjectionType.URL.value].sort()
        self.assertListEqual(expected[ConfigurationExportIdentifier.GLOBAL_PAYLOADS.value][InjectionType.URL.value], actual[ConfigurationExportIdentifier.GLOBAL_PAYLOADS.value][InjectionType.URL.value])
        
        expected[ConfigurationExportIdentifier.GLOBAL_PAYLOAD_FILES.value][InjectionType.URL.value].sort()
        actual[ConfigurationExportIdentifier.GLOBAL_PAYLOAD_FILES.value][InjectionType.URL.value].sort()
        self.assertListEqual(expected[ConfigurationExportIdentifier.GLOBAL_PAYLOAD_FILES.value][InjectionType.URL.value], actual[ConfigurationExportIdentifier.GLOBAL_PAYLOAD_FILES.value][InjectionType.URL.value])
        
        self.assertEqual(expected[ConfigurationExportIdentifier.GLOBAL_PAYLOAD_FILE_SEPARETOR.value], actual[ConfigurationExportIdentifier.GLOBAL_PAYLOAD_FILE_SEPARETOR.value])
        self.assertEqual(expected[ConfigurationExportIdentifier.INJECTORS.value], actual[ConfigurationExportIdentifier.INJECTORS.value])
        
        
        # valori non ordinati nelle liste
        
    
    def test_build_injector(self):
        self.fail("Not implemented")

if __name__ == "__main__":
    unittest.main()