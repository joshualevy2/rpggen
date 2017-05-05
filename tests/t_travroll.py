import sys
import unittest

sys.path.append('..')
from rpggen import Rpggen
from Traveller import Traveller

class TestTravellerRolls(unittest.TestCase):

   def setUp(self):
      # Dice roller always returns this number, so we know what the results should be.
      Rpggen.testData = 2

   def test_1(self):
      result = Traveller.roll()
      self.assertEqual(result, 4)

   def test_2(self):
      result = Traveller.roll(1)
      self.assertEqual(result, 2)
      
   def test_3(self):
      result = Traveller.roll(3)
      self.assertEqual(result, 6)
 
   def test_4(self):
      result = Traveller.roll(target='5-')
      self.assertTrue(result)

   def test_5(self):
      result = Traveller.roll(target='7+')
      self.assertFalse(result)
       
   def test_11(self):
      result = Traveller.roll(dm='+1')
      self.assertEqual(result, 5)

   def test_12(self):
      result = Traveller.roll(dm='-1')
      self.assertEqual(result, 3)
      
   def test_13(self):
      result = Traveller.roll(dm='+0')
      self.assertEqual(result, 4)
 
   def test_14(self):
      result = Traveller.roll(target='5-', dm='+1')
      self.assertTrue(result)

   def test_15(self):
      result = Traveller.roll(target='7+', dm='-1')
      self.assertFalse(result)
            
if __name__ == '__main__':
    unittest.main()