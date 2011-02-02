from taskqueue import Queue
from taskqueue import Task
from time import sleep

def main():
    # ---------
    # Example
    # ---------
    from random import random
    
    def writethis(msg, msgr='anon'):
        sleep(random()*0.5)
        return '%s: %s' % (msgr, msg)

    q=Queue()
    for i in range(10):
        q.append(Task(writethis, (i, 'desu')))
        q.append(Task(writethis, (i,)))

    print 'waiting...'

    q.wait()
    print 'printing...'
    while not q.is_empty():
        print '.',
        print q.pop().result
    print q.is_empty()
    q.die()



if __name__ == '__main__':
    main()










