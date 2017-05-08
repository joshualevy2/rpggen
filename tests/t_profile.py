import sys
import unittest

sys.path.append('..')

from rpggen import Rpggen
from Traveller import Profile, Traveller

class TestProfile(unittest.TestCase):

   def test_1(self):
      one = Profile("testOne", ["A"])
      str = one.generate() 
      self.assertEqual(str, "A")     
      fmt = one.smallStr() 
      self.assertEqual(fmt, "A") 
      
   def test_2(self):
      two = Profile("testTwo", ["A","B","C"])
      str = two.generate() 
      self.assertEqual(str, "ABC")  
      fmt = two.smallStr() 
      self.assertEqual(fmt, "ABC") 
      
   def test_3(self):
      three = Profile("testTwo", ["ABCDE","123456789","abcde","!@#$%^&*"])
      for ii in range(5):
         str = three.generate() 
         fmt = three.smallStr()
         #print('Four letters (letter, number letter, punct: %s %s' % (str, fmt))
         self.assertEqual(len(str), 4)  
      
   def test_1f(self):
      one = Profile("testOne", ["A"],format='%c')
      str = one.generate() 
      self.assertEqual(str, "A")     
      fmt = one.smallStr() 
      self.assertEqual(fmt, "A") 
      
   def test_2f(self):
      two = Profile("testTwo", ["A","B","C"], format='%c-%c-%c')
      str = two.generate() 
      self.assertEqual(str, "ABC")  
      fmt = two.smallStr() 
      self.assertEqual(fmt, "A-B-C") 
      
   def test_3f(self):
      three = Profile("testTwo", ["ABCDE","123456789","abcde","!@#$%^&*"],format='%c%c=%c%c')
      for ii in range(5):
         str = three.generate() 
         fmt = three.smallStr()
         #print('Four letters (letter, number letter, punct: %s %s' % (str, fmt))
         self.assertEqual(len(str), 4)  
         self.assertEqual(len(fmt), 5)


if __name__ == '__main__':
    unittest.main()