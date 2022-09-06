import unittest
from PJ.model.variable import Variable, FixedVariable, InjectableVariable
from PJ.model.url import Url, ExportIdentifier
from PJ.model.configuration import Configuration

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
            ExportIdentifier.URL.value : domain,
            ExportIdentifier.INJECTABLE_VARAIBLE.value : {"ciao": "q"},
            ExportIdentifier.FIXED_VARAIBLE.value : {"hey": "g"}
        }

        self.assertDictEqual(expected, url3.to_dict())
    
    def test_from_dict(self):
        domain = "https://domain"
        
        expected = {
            ExportIdentifier.URL.value : domain,
            ExportIdentifier.INJECTABLE_VARAIBLE.value : {"ciao": "q"},
            ExportIdentifier.FIXED_VARAIBLE.value : {"hey": "g"}
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
            ExportIdentifier.INJECTABLE_VARAIBLE.value : {"ciao": "q"},
            ExportIdentifier.FIXED_VARAIBLE.value : {"hey": "g"}
        }

        self.assertRaises(ValueError, Url.from_dict, (possible_dict))

        possible_dict_1 = {
            ExportIdentifier.URL.value : domain,
            ExportIdentifier.FIXED_VARAIBLE.value : {"hey": "g"}
        }

        self.assertRaises(ValueError, Url.from_dict, (possible_dict_1, False))

        possible_dict_2 = {
            ExportIdentifier.URL.value : domain,
            ExportIdentifier.INJECTABLE_VARAIBLE.value : {"ciao": "q"}
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
    
    def test_missing_version_fd(self):
        relative_path = "src/tests/configrations/no_version_config.json"
        fd = open(relative_path)
        self.assertRaises(ValueError, Configuration.from_file_descriptor, (fd))
    
    def test_missing_Injector_fd(self):
        relative_path = "src/tests/configrations/no_injector_config.json"
        fd = open(relative_path)
        self.assertRaises(ValueError, Configuration.from_file_descriptor, (fd))
    
    def test_missing_name_fd(self):
        relative_path = "src/tests/configrations/no_name_config.json"
        fd = open(relative_path)
        cnf = Configuration.from_file_descriptor(fd)
        self.assertEqual(cnf.config_name, "no_name_config.json")
    
    def test_missing_global_payloads_fd(self):
        relative_path = "src/tests/configrations/no_global_payloads.json"
        fd = open(relative_path)
        cnf = Configuration.from_file_descriptor(fd)
        self.assertEqual({}, cnf.global_payloads)
    
    def test_missing_global_payloads_file_fd(self):
        relative_path = "src/tests/configrations/no_global_payloads_file.json"
        fd = open(relative_path)
        cnf = Configuration.from_file_descriptor(fd)
        self.assertEqual({}, cnf.global_payload_files)
        
    def test_missing_global_payloads_file_separetor_fd(self):
        relative_path = "src/tests/configrations/no_global_payload_file separetor.json"
        fd = open(relative_path)
        cnf = Configuration.from_file_descriptor(fd)
        self.assertEqual("\n", cnf.payload_file_separetor)
    
    def test_missing_version_fn(self):
        relative_path = "src/tests/configrations/no_version_config.json"
        self.assertRaises(ValueError, Configuration.from_file, (relative_path))
    
    def test_missing_Injector_fn(self):
        relative_path = "src/tests/configrations/no_injector_config.json"
        self.assertRaises(ValueError, Configuration.from_file, (relative_path))
    
    def test_missing_name_fn(self):
        relative_path = "src/tests/configrations/no_name_config.json"
        cnf = Configuration.from_file(relative_path)
        self.assertEqual(cnf.config_name, "no_name_config.json")
    
    def test_missing_global_payloads_fn(self):
        relative_path = "src/tests/configrations/no_global_payloads.json"
        cnf = Configuration.from_file(relative_path)
        self.assertEqual({}, cnf.global_payloads)
    
    def test_missing_global_payloads_file_fn(self):
        relative_path = "src/tests/configrations/no_global_payloads_file.json"
        cnf = Configuration.from_file(relative_path)
        self.assertEqual({}, cnf.global_payload_files)
        
    def test_missing_global_payloads_file_separetor_fn(self):
        relative_path = "src/tests/configrations/no_global_payload_file separetor.json"
        cnf = Configuration.from_file(relative_path)
        self.assertEqual("\n", cnf.payload_file_separetor)

    def test_build_injector(self):
        self.fail("Not implemented")

if __name__ == "__main__":
    unittest.main()