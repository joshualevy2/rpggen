import sys
sys.path.append('..')
from Rpggen import Rpggen
from Traveller import Traveller

def testroll(dicestr=None, target=None):
   results = []
   for idx in range(6):
      if dicestr is None:
         results.append(str(Traveller.roll(target)))
      else:
         results.append(str(Traveller.roll(dicestr,target)))
   if dicestr is None:
      dicestr = 'Traveller.default'      
   print('%s target=%s: %s' % (str(dicestr), target, " ".join(results)))
 
# execute only if run as a script    
if __name__ == "__main__":  
    testroll(target='5+')
    testroll(target='5-')
    testroll(target='11+')
    testroll(target='11-')
