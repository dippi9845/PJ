'''
An interface that model a whatever thing that can be injected a payload
'''
class Injectable:

    def __init__(self) -> None:
        raise TypeError("This is an interface, so is not instatiable")

    def _clear():
        pass

    def inject(payload : str):
        pass
