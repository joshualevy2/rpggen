
import sys
import unittest

sys.path.append('..')
from Rpggen import Table, Template, Rpggen

class TestTemplate(unittest.TestCase):

   def setUp(self):
      # Dice roller always returns this number, so we know what the results should be.
      Rpggen.testData = 2

   def test_const(self):

      temp = Template('t1', 'Constant template: nothing changes.')  
      result = temp.use()
      self.assertEqual(result, 'Constant template: nothing changes.')    

   def test_dice(self):
      temp = Template('t1', '''IQ: {{use('3d6')}} DX: {{use('1d10')}} ST: {{use('2d5+2')}}''')  
      result = temp.use()
      self.assertEqual(result, 'IQ: 6 DX: 2 ST: 6')   

   def test_table(self):
      tab = Table('test3', {'1':'one','2': 'two'})
      temp = Template('t1', '''IQ: {{use('test3')}}''')  
      result = temp.use()
      self.assertEqual(result, 'IQ: two')   

if __name__ == '__main__':
    unittest.main()