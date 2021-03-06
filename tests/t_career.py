import unittest
import sys
sys.path.append('..')
from CepheusEngine import Career, CepheusEngine, Character
from CorporateRepo import CorporateRepo
from Rpggen import Rpggen
from Traveller import Traveller

class TestCareer(unittest.TestCase):
   '''This class tests the Career class, using CorporateRepo as a sample
      career, for test purposes.
   '''
    
   def setUp(self):
      # Dice roller always returns this number, so we know what the results should be.
      Rpggen.testData = 2 
      # Initialize the CepheusEngine environment, which also initializes the 
      # basic Traveller environment.
      self.cepheusEngine = CepheusEngine()
 
      # Initialize the CorporateRepo career
      self.crCareer = CorporateRepo()
 
      # Create an (empty) character to start with.
      #self.crPerson = Character()      
    
    
   def test_roll(self):
       '''Tests the roll method of careers (not the one for Traveller or
          Rpggen).
       '''
       Rpggen.testData = 2
       result = self.crCareer.roll('reenlistment')
       self.assertFalse(result)  

       Rpggen.testData = 4
       result = self.crCareer.roll('reenlistment')
       self.assertTrue(result)         


if __name__ == '__main__':
    unittest.main()