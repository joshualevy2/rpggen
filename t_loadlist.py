import unittest

from rpggen import Rpggen

class TestLoadList(unittest.TestCase):

   def setUp(self):
      # Dice roller always returns this number, so we know what the results should be.
      Rpggen.testData = 2

   def test_1(self):
      Rpggen.loadlist('test1', ['one','two'])
      print(Rpggen.finduse('test1'))
      
   def test_2(self):
      # Try to get the wrong answer 1000 times
      Rpggen.loadlist('test2', ['one','two'])
      for rr in range(1000):
          result = Rpggen.finduse('test2')
          self.assertEqual(result,"two")     
            
if __name__ == '__main__':
    unittest.main()