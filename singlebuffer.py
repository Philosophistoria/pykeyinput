class SingleBuffer:
    def __init__(self, arg_initdata=None):
        self.__data = arg_initdata

    def write(self, arg_data):
        self.__data = arg_data

    def read(self):
        return self.__data

    def flush(self):
        self.__data = None

    def readable(self):
        return self.__data != None
    