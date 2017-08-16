
import logging
import sys
import unittest

sys.path.append('..')
from Rpggen import Table, Rpggen

class TestTableLt(unittest.TestCase):

   def setUp(self):
      # Dice roller always returns this number, so we know what the results should be.
      Rpggen.testData = 2
      #logging.basicConfig(level=logging.DEBUG)

   def test_basic(self):
      tab = Rpggen.loadLt('../samples/PersonalityTraits.lt')
      res1 = tab.use()
      self.assertEqual(res1,'Abrasive')
      res2 = tab.use()
      self.assertEqual(res2,'Abrasive')
      values = tab.results()
      #values.sort()
      self.assertEqual(len(values),400)  

   def test_removeFirstToken(self):
      tab = Rpggen.loadLt('../samples/PersonalityTraits100.lt')
      res1 = tab.use()
      print(res1)
      self.assertEqual(res1,'Always Betray Rebel Scum')
      res2 = tab.use()
      print(res2)
      self.assertEqual(res2,'Always Betray Rebel Scum')
      values = tab.results()
      #values.sort()
      self.assertEqual(len(values),100) 

if __name__ == '__main__':  
   unittest.main()