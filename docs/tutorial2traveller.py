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
import sys
sys.path.append('..')
from Rpggen import Rpggen, Dice, Table, Template, Select

