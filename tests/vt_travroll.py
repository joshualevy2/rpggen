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
   print('%s target=%s: %s' % (str(dicestr), target, " ".join(results)))
 
# execute only if run as a script    
if __name__ == "__main__":  
    testroll(target='5+')
