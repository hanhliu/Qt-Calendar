
class MainController:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.list_divisions = []
        return cls.__instance
