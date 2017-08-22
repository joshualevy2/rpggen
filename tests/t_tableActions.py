
import logging
import sys
import unittest

sys.path.append('..')
from Rpggen import Table, Rpggen

class TestTableActions(unittest.TestCase):

   def setUp(self):
      # Dice roller always returns this number, so we know what the results should be.
      Rpggen.testData = 2
      #logging.basicConfig(level=logging.DEBUG)
      self.allTables = []
      self.tab1 = Table("test1", ['one','two','three','four'])
      self.allTables.append(self.tab1)
      self.tab2 = Table("test2", {'1':'one','2': 'two'})
      self.allTables.append(self.tab2)
      self.tab3 = Table("test3", {'roll': '1d4', '1-2':'two', '3-4': 'four'})
      self.allTables.append(self.tab3)

   def test_names(self):
      values = Table.names()
      self.assertEqual(values,'test1, test2, test3')


   def test_results1(self):
      results = self.tab1.results()
      results.sort()
      self.assertEqual(results,['four','one','three','two'])

   # todo: repeat for all other tables   
       

if __name__ == '__main__':
    unittest.main()