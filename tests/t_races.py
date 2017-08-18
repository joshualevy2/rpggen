import sys
import unittest

sys.path.append('..')

from CepheusEngine import CepheusEngine
from Traveller import Traveller
from Rpggen import Rpggen

class TestRaces(unittest.TestCase):

    def test_traveller(self):
       
       # Characters start out with no money.
       major = Traveller.majorRaces
       print(major)
       #self.assertEqual(money, 0)

       minor = Traveller.minorRaces
       print(minor)
       #self.assertEqual(money, 0)

       races = Traveller.races
       print(races)
       #self.assertEqual(money, 0)       
       
    def test_cepheusEngine(self):
       
       # Characters start out with no money.
       major = CepheusEngine.majorRaces
       print(major)
       #self.assertEqual(money, 0)

       minor = CepheusEngine.minorRaces
       print(minor)
       #self.assertEqual(money, 0)

       races = CepheusEngine.races
       print(races)
       #self.assertEqual(money, 0)       

if __name__ == '__main__':
    Rpggen.testData = 2
    unittest.main()