import sys
sys.path.append('..')
import taskqueue

queue = taskqueue.Queue() # setup a queue

for i in range(10):
    queue.add(pow, i, 2) # add Task()s to the queue


for task in queue.finished: # itereate over the finished tasks
    print task.result # print the result