import threading

class QueueBuffer:
    def __init__(self, arg_initdata=None, arg_max_len=100):
        if arg_initdata == None or arg_initdata == []:
            self.__data = []
        else:
            self.__data = arg_initdata

        self.__max_len = arg_max_len
        self.ev = threading.Event()
        self.debug = False

    def write(self, arg_data):
        self.__data += [arg_data]
        if (len(self.__data) > self.__max_len):
            print('buffer overflow')
            retval = self.read() 
        else:
            retval = None
        self.ev.set()
        if self.debug:
            print(self._check_dump(), retval, "in wirte")
        return retval

    def read(self):
        if len(self.__data ) > 0:
            retval = self.__data[0]
            self.__data = self.__data[1:]
        else:
            retval = None
        if len(self.__data) == 0:
            self.ev.clear()
        if self.debug:
            print(self._check_dump(), retval, "in wirte")
        return retval

    def _check_dump(self):
        return self.__data

    def flush(self):
        self.__data = [] 

    def readable(self):
        return len(self.__data) > 0

    def readable_len(self):
        return len(self.__data)

    def wait_new_data(self):
        if len(self.__data) == 0:
            self.ev.wait()
