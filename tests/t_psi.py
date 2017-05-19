import sys
import unittest
import json

sys.path.append('..')
from CepheusEngine import Character
from Rpggen import Rpggen

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

if __name__ == '__main__':
    Rpggen.testData = 2
    unittest.main()