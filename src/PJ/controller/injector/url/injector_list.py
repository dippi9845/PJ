from single_url_injector import SingleUrlInjector
from ....model.injectable.injectable_variable import InjectableVariable

class InjectorList:
    def __init__(self, injectors : list[SingleUrlInjector]):
        self.__injectors = injectors

    def inject_all(self):
        for i in self.__injectors:
            i.inject_all()
    
    def split(self, num : int) -> list:
        rtr = [self.__injectors[x:x+num] for x in range(0, len(self.__injectors), num)]
        rtr = map(lambda x: InjectorList(x.copy()), rtr)
        return rtr


def by_values(urls : list[str], payloads : list[list[str]], vars : list[list[InjectableVariable]], vars_in_url_are_fixed=True, fixed_vars=[[]]) -> InjectorList:
    return InjectorList(map(lambda u, p, v, fv: SingleUrlInjector(u,p,v,vars_in_url_are_fixed=vars_in_url_are_fixed, fixed_vars=fv), urls, payloads, vars, fixed_vars))

def by_values(urls : list[str], payloads : list[str], vars : list[list[InjectableVariable]], vars_in_url_are_fixed=True, fixed_vars=[[]]) -> InjectorList:
    return InjectorList(map(lambda u, v, fv: SingleUrlInjector(u, payloads, v, vars_in_url_are_fixed=vars_in_url_are_fixed, fixed_vars=fv), urls, vars, fixed_vars))