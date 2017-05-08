
import sys
import unittest

sys.path.append('..')
from rpggen import Select, Rpggen

class TestSelect(unittest.TestCase):

   def setUp(self):
      # Dice roller always returns this number, so we know what the results should be.
      Rpggen.testData = 2

   def test_choose1(self):
      res1 = Select.choose(['one','two','three','four'])
      self.assertEqual(res1,'two')
      res2 = Select.choose(['one','two','three','four'])
      self.assertEqual(res2,'two')   

if __name__ == '__main__':
    unittest.main()