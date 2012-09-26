import taskqueue

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
    
    q = taskqueue.Queue()
    
    q.add(euler5, 9)
    
    q.wait()
    
    for task in q.finished:
        print task.result
    


if __name__ == '__main__':
    main()










