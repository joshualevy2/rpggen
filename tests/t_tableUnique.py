
import logging
import sys
import unittest

sys.path.append('..')
from Rpggen import Table, Rpggen

class TestTableUnique(unittest.TestCase):

   def setUp(self):
      # Dice roller always returns this number, so we know what the results should be.
      Rpggen.testData = 2
      #logging.basicConfig(level=logging.DEBUG)

   def test_uniqueList1(self):
      tab = Table("test1", ['one','two','three','four'], unique=True)
      res1 = tab.use()
      self.assertEqual(res1,'two')
      res2 = tab.use()
      self.assertEqual(res2,'one')     

   def test_uniqueList2(self):
      tab = Table("test1", ['one','two','three','four'], unique=False)
      res1 = tab.use()
      self.assertEqual(res1,'two')
      res2 = tab.use()
      self.assertEqual(res2,'two') 

   def test_uniqueList3(self):
      tab = Table("test1", ['one','two','three','four'], unique=True)
      res1 = tab.use()
      self.assertEqual(res1,'two')
      tab.clear()
      res2 = tab.use()
      self.assertEqual(res2,'two') 

   def test_uniqueFull(self):
      tab = Table("test8", ['one','two','three','four'], unique=True)
      res1 = tab.use()
      self.assertEqual(res1,'two')
      res2 = tab.use()
      self.assertEqual(res2,'one') 
      res3 = tab.use()
      self.assertEqual(res3,'three')    
      res4 = tab.use()
      self.assertEqual(res4,'four') 

   def test_uniqueFull2(self):
      tab = Table("test8", ['one','two','three','four'], unique=True)
      res1 = tab.use()
      self.assertEqual(res1,'two')
      res2 = tab.use()
      self.assertEqual(res2,'one') 
      res3 = tab.use()
      self.assertEqual(res3,'three')    
      res4 = tab.use()
      self.assertEqual(res4,'four') 
      # Expect/want the exception here
      self.assertRaises(ValueError,tab.use)

if __name__ == '__main__':
    unittest.main()