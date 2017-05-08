import sys
import unittest
import json

sys.path.append('..')
from rpggen import Rpggen
from Traveller import Attribute, Traveller

class TestPsi(unittest.TestCase):

   def test_1(self):
      attr = Attribute("Fighting", 3)
      self.assertEqual(attr.strAttr(), 'Fighting-3')

   def test_2(self):
      attr = Attribute('Fighting (Right Handed)', 1)
      self.assertEqual(attr.strAttr(), 'Fighting (Right Handed)-1') 

if __name__ == '__main__':
    unittest.main()