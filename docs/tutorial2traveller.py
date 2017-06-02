# This python program is BOTH a program you can run, and tutorial you can read.
# The code runs, and the comments are the tutorial.
#
# This file covers the Traveller and CepheusEngine libraries.
#

# Rpggen is the basic class that has functions useful to all Role Playing Games.
# It includes the following functionality:
#    * Rolling Dice
#    * Using (Rolling on) Tables
#    * Using Templates
#    * Selecting from Lists
#


# The python file Traveller contains data and functions which are general to 
# the Traveller Role Playing Game.  The python file CepheusEngine includes
# data and functions which are specific to the CepheusEngine version of 
# Traveller.  CephenusEngine inherits from Traveller when the rules are the
# same.  If you want to use ClassTraveler rules (from the LBBs), then you
# should use the Traveller file instead of CepheusEngine, below:

import sys
sys.path.append('..')
from CepheusEngine import Career, Character
from Traveller import Traveller

# TODO: do we need that Traveller line above?


