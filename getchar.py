#__all__ = ["getChar", "ttyrese"]


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()
    
    def __del__(self):
        del self.impl

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys, termios
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
    

    def __del__(self):
        import sys, tty, termios
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
        print("delete get char obj")


    def __call__(self):
        import sys, tty, termios
        try:
            #print("== single key mode ==\n")
            #   Raw mode is extremely raw, changing stdout to raw as well as stdin, 
            #   which makes "\n" just a LF without CR.
            #tty.setraw(sys.stdin.fileno())
            #
            #   C-break mode is more appropreate for this 
            #   because This mode also allow us to use ^C break
            #   Also, it doesn't change stdout behaviour (stay rich alittle bit)
            tty.setcbreak(self.fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            #termios.tcsetattr(fd, termios.TCSANOW, old_settings)
            #print("== till-enter mode ==\n")
            pass
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


'''
_getchar = _Getch()


def getChar()->str:
    return _getchar()


def ttyreset():
    global _getchar
    del _getchar

'''