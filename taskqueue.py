from threading import Thread
from time import time, sleep
from multiprocessing import cpu_count

class Queue(Thread):
    def __init__(self, **kwargs):
        Thread.__init__(self)
        
        # SET THE DEFAULT NUMBER OF WORKERS
        if "workers" in kwargs and int(kwargs["workers"])>0:
            self.num_workers = kwargs["workers"]
        else:
            self.num_workers = cpu_count()*2 # DEFAULT TWO WORKERS PER CPU
        
        if "idle_timeout" in kwargs and int(kwargs["idle_timeout"])>=0: # ALLOW FOR ZERO WAIT TIME
            self.idle_timeout = kwargs["idle_timeout"]
        else:
            self.idle_timeout = 1 # DEFAULT 
        
        # NO NEED FOR FANCY STUFF
        self.waiting = list()
        self.running = list()
        self._finished = list()
        
        # LSTS
        self.dying = False
        self.start()

    def run(self):
        do_sleep = False
        while True:
            # MOVE FINISHED TASKS OUT OF THE RUNNING LIST
            for task in self.running:
                if not task.is_alive():
                    self._finished.append(task)
                    self.running.remove(task)
                    do_sleep = True
            
            # ADD TASKS TO THE RUNNING LIST
            if not do_sleep and len(self.waiting)>0 and len(self.running)<self.num_workers:
                do_sleep = True
            while len(self.waiting)>0 and len(self.running)<self.num_workers:
                task = self.waiting.pop(0)
                self.running.append(task)
                task.start()
            
            # IF NO TASKS RUNNING OR WWAITING SET TIMEOUT START TIME
            if self.idle and not self.dying:
                self.dying = True
                self.idle_start = time()
            # IF TIMEOUT HAS BEEN SET AND THERE ARE NEW TASKS RUNNING OR WAITING TO RUN STOP THE TIMEOUT CHECKER
            elif not self.idle and self.dying:
                self.dying = False
            
            # IF NOTHING WAS DONE PAUSE THE LOOP FOR A WHILE
            if do_sleep:
                sleep(0.1) # KEEP THIS INTERVAL SHORT BUT NOT TOO SHORT
            
            # CHECK IF TIMEOUT INTERVAL HAS PASSED
            if self.idle and self.dying and time()-self.idle_start>self.idle_timeout:
                break # THE LOOP
    
    
    def add(self, target, *args):
        self.waiting.append(Task(target, *args))
    
    
    def wait(self):
        while not self.idle:
            sleep(0.1)
    
    @property
    def idle(self):
        return len(self.waiting)==0 and len(self.running)==0
    
    @property
    def finished(self):
        cursor = 0
        while True:
            if cursor<len(self._finished):
                yield self._finished[cursor]
                cursor+=1
            elif self.idle and cursor>=len(self._finished):
                break
            else:
                sleep(0.1)


class Task(Thread):
    def __init__(self, target, *args):
        Thread.__init__(self)
        self.target = target
        self.args = args


    def run(self):
        try:
            self._result = self.target(*self.args)
        except BaseException, e:
            self._result= e
        return self


    @property
    def result(self):
        while self.is_alive():
            sleep(0.5)
        return self._result


