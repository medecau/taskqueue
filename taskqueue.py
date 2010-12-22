# -*- coding: utf-8 -*-
license='''
Copyright (c) 2010 Pedro Rodrigues

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

'''

from threading import Thread
from collections import deque
from time import sleep
from multiprocessing import cpu_count

class Queue(Thread):
    normal=deque()
    finished=deque()
    _die=False
    
    def __init__(self, name=None, items=None, num_workers=None):
        Thread.__init__(self)
        if items:
            self.normal.append(items)
        else:
            pass
        if num_workers is not None:
            self.num_workers=num_workers
        else:
            try:
                self.num_workers=cpu_count()*2
            except:
                self.num_workers=2
        self.live=[]
        self.start()
    
    def run(self):
        while not self._die:
            sleep(0.1)
            index=0
            while index < len(self.live): # remove finished tasks from live stage
                task=self.live[index]
                if not task.is_alive():
                    self.live.pop(index)
                    self.finished.append(task)
                else:
                    index+=1
            while len(self.live)<self.num_workers and len(self.normal)>0:      # run activate tasks in live stage
                try:
                    next_task=self.normal.popleft()
                    next_task.start()
                    self.live.append(next_task)
                except IndexError:
                    pass # no Tasks in queue
    
    def append(self, item):
        if type(item) is type(iter('')) or type(item) is type(list()):
            self.normal.extend(iter(item))
        else:
            self.normal.append(item)
    
    def pop(self):
        while not self.is_empty():
            try:
                return self.finished.popleft()
            except IndexError:
                sleep(0.1)
    
    def wait(self):
        while (not self._die and len(self.normal)>0) or len(self.live)>0:
            sleep(0.1)
        self.die()
    
    def is_empty(self):
        if len(self.normal)+len(self.finished)+len(self.live)>0:
            return False
        else:
            return True
    def die(self):
        self._die=True


class Task(Thread):
    _result=None
    
    def __init__(self, target, name=None, args=None):
        Thread.__init__(self)
        self.target=target
        self.args=args
    
    def run(self):
        self._result=self.target(*self.args)
        return self
    
    def wait(self):
        try:
            self.join(100)
        except:
            pass
        return self
    
    def _get_result(self):
        return self._result
    
    result = property(_get_result)




