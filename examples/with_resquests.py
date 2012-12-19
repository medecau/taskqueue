import sys
sys.path.append('..')
import requests
import taskqueue

s = requests.session()
q = taskqueue.Queue()
q.add(s.get, 'http://example.com/')

for t in q.finished:
    print t.result.text
