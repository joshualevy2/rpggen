import sys
sys.path.append('..')
from Rpggen import Rpggen
from Traveller import Traveller

def testroll(dicestr, target=None):
   results = []
   for idx in range(6):
      results.append(str(Traveller.roll(dicestr,target)))
   print('%s target=%s: %s' % (str(dicestr), target, " ".join(results)))
 
# execute only if run as a script    
if __name__ == "__main__":  
    testroll(1)
    testroll(2)
    testroll(2, '5+')
    testroll(target='5+')
