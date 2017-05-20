import sys
sys.path.append('..')
from Rpggen import Rpggen

def testroll(dicestr) :
    print(dicestr+": "+str(Rpggen.roll(dicestr))+" "+str(Rpggen.use(dicestr))+" "+str(Rpggen.finduse(dicestr))+
                  " "+str(Rpggen.roll(dicestr))+" "+str(Rpggen.use(dicestr))+" "+str(Rpggen.finduse(dicestr)))
 
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
    testroll("1d3+17") 
    testroll("17d3") 
    testroll("d66")
    if False:   # 'o' is not yet supported
       testroll("2o3d6")
       testroll("3o4d6")
    print('Set d66support=True')
    Rpggen.setCustomization('d66support',True)
    testroll("d66")
