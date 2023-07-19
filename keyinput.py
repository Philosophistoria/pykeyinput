#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import time
import sys
import threading
import signal
import fcntl
import os

from .getchar import _Getch


class KeyListener (threading.Thread):
    def __init__(self, out = sys.stdout, eol = ''):
        # out: requires an object which has method 'write()'; e.g. sys.stdout, buffer classes
        # eol: is supposed an str; this is appended to the end of the line output by the `out` above

        super(KeyListener,self).__init__()

        if (not hasattr(out, 'write') or not callable(out.write)):
            out = sys.stdout
        self.output_src = out

        if (not type(eol) == str):
            eol = ''
        self.eol = eol

        self.isListening = True
        self.__Listening = threading.Event()

        # invoke handle_io on a SIGIO event
        signal.signal(signal.SIGIO, self.handle_event)
        # send io events on stdin (fd 0) to our process 
        assert fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETOWN, os.getpid()) == 0
        # tell the os to produce SIGIO events when data is written to stdin
        assert fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, os.O_ASYNC) == 0

        self.getChar = _Getch()

    def __del__(self):
        print("key listener is killed")
        del self.getChar

    def run(self):
        while True:
            # if set, the event should be cleared so as to wait again later
            self.__Listening.clear()
            # stop until having it set
            self.__Listening.wait()

            if not self.isListening:
                break
                
            value = str(self.getChar())
            self.output_src.write(value + self.eol)


    def keepListening(self):
        self.isListening = True
        self.__Listening.set()


    def stopListening(self):
        self.isListening = False
        self.__Listening.clear()


    def handle_event(self, signal, frame):
        self.__Listening.set()


    def terminate(self):
        self.isListening = False
        self.__Listening.set()


    def giveEar(self):
        self.__Listening.set()
    

class PromptView:
    def __init__(self, prompt_style="> "):
        # buffer: requires a method "deligate" which accept a function as an argument
        # prompt_style: is str being supposed to be showed as prompt

        self.showevent = threading.Event()

        if (type(prompt_style) != str):
            prompt_style = "> "
        self.__style = prompt_style


    def showPrompt(self,towait=True):
        # show the prompt
        sys.stdout.write(self.__style)
        sys.stdout.flush()
        if towait:
            # then, stop until having it set
            # clear the event flag so as it can wait avoiding unlimited loop
            self.showevent.clear()
            self.showevent.wait()


# Usage
'''
Modules/../$ python3 -m Modules.keyinput
'''
if __name__ == "__main__":
    from . import singlebuffer, queuebuffer
    from .pyobservable import observable, observer
    prompt = PromptView('neko > ')
    buf = observable.ObservableNotifier(queuebuffer.QueueBuffer())
    buf.attatch(observer.receive_notification_by(prompt.showevent.set,attr_res='write',timing_res='post'))
    keylistener = KeyListener(buf, '')
    keylistener.daemon=True
    keylistener.start()
    loop_state = '0'
    try:
        while True:
            buf.flush()
            prompt.showPrompt()
            data = buf.read()
            print(ord(data))

            if data != None and '0' < data and data < '9':
                loop_state = data

            if ord(data) == 27 :
                while not buf.readable_len() >= 2:
                    pass
                if ord(buf.read()) == 91:
                    data = buf.read()
                    if ord(data) == 65:
                        print("UP\n")
                    if ord(data) == 66:
                        print("DOWN\n")
                    if ord(data) == 67:
                        print("RIGHT\n")
                    if ord(data) == 68:
                        print("LEFT\n")

            while '0' < loop_state and loop_state < '9':
                if(buf.readable()):
                    data = buf.read()
                else:
                    data = "no data"
                print("\n")
                print(data + ' data == \'E\' : ' + str(data == 'E'))
                print('\r')
                if data == 'E':
                    loop_state = '0'
                time.sleep(1)
            
            if data == 'q':
                break

    except KeyboardInterrupt:
        pass