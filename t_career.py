import unittest

from CepheusTraveller import Career, CepheusTraveller, Character
from CorporateRepo import CorporateRepo
from rpggen import Rpggen
from Traveller import Traveller

class TestCareer(unittest.TestCase):
   '''This class tests the Career class, using CorporateRepo as a sample
      career, for test purposes.
   '''
    
   def setUp(self):
      # Dice roller always returns this number, so we know what the results should be.
      Rpggen.testData = 2 
      # Initialize the CepheusTraveller environment, which also initializes the 
      # basic Traveller environment.
      self.cepheusTraveller = CepheusTraveller()
 
      # Initialize the CorporateRepo career
      self.crCareer = CorporateRepo()
      self.crCareer.setup()
 
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