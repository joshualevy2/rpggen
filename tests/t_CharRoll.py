import sys
import unittest

sys.path.append('..')
from CepheusEngine import CepheusEngine, Character
from rpggen import Rpggen

class TestCharacterRoll(unittest.TestCase):

   def setUp(self):
      # Dice roller always returns this number, so we know what the results should be.
      Rpggen.testData = 2
      cepheusEngine = CepheusEngine()
      self.corpRepo = Character()
      self.corpRepo.int = 7
      self.corpRepo.dex = 12

   def test_1(self):
      result = self.corpRepo.roll('int','9+')
      self.assertFalse(result)

   def test_2(self):
      result = self.corpRepo.roll('dex','2+')  
      self.assertTrue(result)

   # TODO: add more tests  each DM different attr and targets.
    
            
if __name__ == '__main__':
    unittest.main()