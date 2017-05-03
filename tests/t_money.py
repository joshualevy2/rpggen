import unittest

from CepheusTraveller import Character
from rpggen import Rpggen
from Traveller import Traveller

class TestMoney(unittest.TestCase):

    def test_1(self):
       corpRepo = Character()
       
       # Characters start out with no money.
       money = corpRepo.availableMoney()
       self.assertEqual(money, 0)
       
       # Makefile sure some basic math works
       corpRepo.money['pocket'] = 1
       corpRepo.money['bank'] = 1
       self.assertEqual(corpRepo.availableMoney(), 2)
       
if __name__ == '__main__':
    Rpggen.testData = 2
    unittest.main()