import sys
import unittest

sys.path.append('..')
from CepheusTraveller import Character
from rpggen import Rpggen
from Traveller import Traveller

class TestDiceRolls(unittest.TestCase):

   def setUp(self):
      # Dice roller always returns this number, so we know what the results should be.
      Rpggen.testData = 2

   def test_1(self):
      result = Rpggen.roll('1d6')
      self.assertEqual(result, 2)

   def test_2(self):
      result = Rpggen.roll('2d6')
      self.assertEqual(result, 4)
      
   def test_3(self):
      result = Rpggen.roll('2d6+1')
      self.assertEqual(result, 5)
 
   def test_4(self):
      result = Rpggen.roll('2d6-1')
      self.assertEqual(result, 3)

   def test_5(self):
      result = Rpggen.roll('d6')
      self.assertEqual(result, 2)
       
   def test_11(self):
      result = Rpggen.roll('1d10')
      self.assertEqual(result, 2)

   def test_12(self):
      result = Rpggen.roll('2d10')
      self.assertEqual(result, 4)
      
   def test_13(self):
      result = Rpggen.roll('2d10+1')
      self.assertEqual(result, 5)
 
   def test_14(self):
      result = Rpggen.roll('2d10-1')
      self.assertEqual(result, 3)

   def test_15(self):
      result = Rpggen.roll('d10')
      self.assertEqual(result, 2)

class TestDiceRolls3(unittest.TestCase):

   def setUp(self):
      # Dice roller always returns this number, so we know what the results should be.
      Rpggen.testData = 3

   def test_1(self):
      result = Rpggen.roll('1d6')
      self.assertEqual(result, 3)

   def test_2(self):
      result = Rpggen.roll('2d6')
      self.assertEqual(result, 6)
      
   def test_3(self):
      result = Rpggen.roll('2d6+1')
      self.assertEqual(result, 7)
 
   def test_4(self):
      result = Rpggen.roll('2d6-1')
      self.assertEqual(result, 5)

   def test_5(self):
      result = Rpggen.roll('d6')
      self.assertEqual(result, 3)
       
   def test_11(self):
      result = Rpggen.roll('1d10')
      self.assertEqual(result, 3)

   def test_12(self):
      result = Rpggen.roll('2d10')
      self.assertEqual(result, 6)
      
   def test_13(self):
      result = Rpggen.roll('2d10+1')
      self.assertEqual(result, 7)
 
   def test_14(self):
      result = Rpggen.roll('2d10-1')
      self.assertEqual(result, 5)

   def test_15(self):
      result = Rpggen.roll('d10')
      self.assertEqual(result, 3)
            
if __name__ == '__main__':
    unittest.main()