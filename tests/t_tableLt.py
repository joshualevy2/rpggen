
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

   def twicetest(self,table,result,entries):
      res1 = table.use()
      self.assertEqual(res1,result)
      res2 = table.use()
      self.assertEqual(res2,result)
      values = table.results()
      self.assertEqual(len(values),entries) 

   def test_basic(self):
      tab = Rpggen.loadLt('../samples/PersonalityTraits.lt')
      self.twicetest(tab,'Abrasive',399)

   def test_removeFirstToken(self):
      tab = Rpggen.loadLt('../samples/PersonalityTraits100.lt')
      self.twicetest(tab,'Always Betray Rebel Scum',100)   

   def test_blank1(self):
      tab = Rpggen.loadLt('lt-files/blank1.lt')
      self.twicetest(tab,'two',2)    

   def test_blank2(self):
      tab = Rpggen.loadLt('lt-files/blank2.lt')
      self.twicetest(tab,'two',2)   

if __name__ == '__main__':  
   unittest.main()