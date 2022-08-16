import unittest
from PJ.model.variable import Variable, FixedVariable, InjectableVariable
from PJ.model.url import Url, ExportIdentifier

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
            ExportIdentifier.URL.value : {
                ExportIdentifier.URL.value : domain,
                ExportIdentifier.INJECTABLE_VARAIBLE.value : {"ciao": "q"},
                ExportIdentifier.FIXED_VARAIBLE.value : {"hey": "g"}
            }
        }

        self.assertDictEqual(expected, url3.to_dict())
    
    def test_from_dict(self):
        self.fail("not implemented")
    
    def test_inject(self):
        self.fail("not implemented")
    
    def test_str(self):
        self.fail("not implemented")


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
    pass


if __name__ == "__main__":
    unittest.main()