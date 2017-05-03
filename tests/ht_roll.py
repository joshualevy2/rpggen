import sys
sys.path.append('..')
from rpggen import Rpggen

def testroll(dicestr) :
    print(dicestr+": "+str(Rpggen.roll(dicestr))+" "+str(Rpggen.use(dicestr))+" "+str(Rpggen.finduse(dicestr)))
 
# execute only if run as a script    
if __name__ == "__main__":     
    testroll("1d10")
    testroll("d6")
    testroll("3d6")
    testroll("1d4+10")
    testroll("1d4-10")
    testroll("2d4")
    testroll("1d100")
    testroll("1d1000")
    testroll("1d7")        
    

