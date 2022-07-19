'''
An interface that model a whatever thing that can be injected a payload
'''
class Injectable:

    def _clear():
        raise NotImplementedError("need to be implemented by superclass")

    def inject(payload : str):
        raise NotImplementedError("need to be implemented by superclass")
