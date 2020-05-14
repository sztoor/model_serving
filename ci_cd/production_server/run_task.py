from workerA import add_nums
import time
if __name__ == '__main__':
    for _ in range(1):
        result = add_nums.delay(10,22)
        time.sleep(2)
        print ('Task finished?',result.ready())
        print ('Task result:',result.result)
        print ('get result"',result.get(timeout=1))
