import sys
sys.path.append('..')
from rpggen import Rpggen

def testchars1(num) :
    print("chars({0}): {1}".format(num,Rpggen.chars(num)))
    
def testchars2(num,fro) :
    print("chars({0},{1}): {2}".format(num,fro,Rpggen.chars(num,fro)))    
 
# execute only if run as a script    
if __name__ == "__main__": 
    testchars1(1)
    testchars1(4)
    testchars1(10)
    testchars2(10,"01")
    testchars2(10,"0123456789ABCDEF")
       
    

