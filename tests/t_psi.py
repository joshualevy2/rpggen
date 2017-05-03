import unittest

from CepheusTraveller import Character
from rpggen import Rpggen
from Traveller import Traveller

class TestPsi(unittest.TestCase):

    def test_upper(self):
       corpRepo = Character()
       corpRepo.createRandomlyTopdown()
       
       # By default, the UPP has six characters (XXXXXX):
       upp = corpRepo.strUpp()
       self.assertEqual(len(upp), 6)
       
       # But if we add PSI to the character, then it should have eight (XXXXXX-X):
       corpRepo.psi = 8
       upp = corpRepo.strUpp()
       self.assertEqual(len(upp), 8)       
       print('UPP = '+upp)
       

#    def test_isupper(self):
 #       self.assertTrue('FOO'.isupper())
  #      self.assertFalse('Foo'.isupper())
#
 #   def test_split(self):
  #      s = 'hello world'
   #     self.assertEqual(s.split(), ['hello', 'world'])
    #    # check that s.split fails when the separator is not a string
     #   with self.assertRaises(TypeError):
      #      s.split(2)

if __name__ == '__main__':
    Rpggen.testData = 2
    unittest.main()