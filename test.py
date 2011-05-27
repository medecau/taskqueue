from taskqueue import Queue
from taskqueue import Task
from time import time, sleep

def euler5(n):
    init=time()
    divs=range(n,0,-1)
    for e in divs:
        for f in divs[::-1]:
            if e%f==0 and e!=f:
                divs.remove(f)

    num=0
    not_found=True
    while not_found:
        num+=n
        not_found=False
        for each in divs:
            if num%each!=0:
                not_found=True
                break

    return (time()-init, num)

def main():
    # ---------
    # Example
    # ---------
    from random import random
    init=time()
    q=Queue()
    for i in range(6):
        q.append(Task(euler5, (17,)))
        q.append(Task(euler5, (11,)))

    print 'waiting...'

    q.wait()
    print 'printing...'
    while not q.is_empty():
        print 'took: %f - value: %d' % q.pop().result
    q.die()
    print 'total running time: %f' % (time()-init)


if __name__ == '__main__':
    main()










