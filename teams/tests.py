from django.test import TestCase
from multiprocessing import Process
import time
from jasper.toolbox import f

class TeamsTestCase(TestCase):
    def test_teams(self):
        print('psv')
        
        p = Process(target=f, args=('bob',))
        time.sleep(1)
        print('testje')
        time.sleep(1)
        p.start()
        time.sleep(1)
        print('wat een kneus')
        #p.join()
        return 1    
        
        
       # def solve1(A):
       #     #f = open("myfile1.txt", "x")
       #     time.sleep(1)
       #     #f.write("Now the file has more content!")
       #     #f.close()
       #     return 1
       #
       # def solve2(B):
       #    # f = open("myfile2.txt", "x")
       #     time.sleep(1)
       #    # f.write("Now the file has more content!")
       #    # f.close()
       #     return 2
       #
       # A =''
       # B =''
       #
       # pool = Pool()
       # result1 = pool.apply_async(solve1, [A])    # evaluate "solve1(A)" asynchronously
       # result2 = pool.apply_async(solve2, [B])    # evaluate "solve2(B)" asynchronously
       # time.sleep(30)
       # answer1 = result1.get(timeout=10)
       # answer2 = result2.get(timeout=10)
       #
       # print('t1 ',answer1)
       # print('t2 ',answer2)
       


#https://stackoverflow.com/questions/20548628/how-to-do-parallel-programming-in-python
#https://sebastianraschka.com/Articles/2014_multiprocessing.html

## https://stackoverflow.com/questions/31097511/python-multiprocessing-cant-find-error