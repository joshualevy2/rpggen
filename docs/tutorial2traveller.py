# This python program is BOTH a program you can run, and tutorial you can read.
# The code runs, and the comments are the tutorial.
#
# This file covers the Traveller and CepheusEngine libraries.
#

# Traveller is the class that has functions useful for the Traveller Role PLaying Game.
# It includes the following functionality:
#    * Careers
#    * Characters
#    * Traveller itself (basic rules and dice rolling)
#    * Profiles (general support for Universal World Profiles, etc.)
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

# Let's start out with the basic Traveller functionality.

# In traveller, the default roll is two dice, so if you just say roll, it is 2d6:
print("Defaut Traveller roll, which is 2d6: %d" % Traveller.roll())

#print("Roll 2 dice: %d" % Traveller.roll(2))

# Traveller has target numbers, like you must roll 8 or higher:
print("Roll 8+ on 2 dice %s" % Traveller.roll('8+'))
# Notice that this returns true or false, not the actual number.

# Traveller also has dice modifiers, for adding +2 to your roll:
print("Roll 8+ with a dice modifier of +2 %s" % Traveller.roll('8+', +2))

# Using Python's named arguments, you can change the order of the arguments,
# if you want to:
print("Roll 8+ with a dice modifier of +2 %s" % Traveller.roll(dm=+2, target='8+'))

#And the dice modifier can be a string, if you prefer:
print("Roll 10+ with a dice modifier of -2 %s" % Traveller.roll(dm='-2', target='8+'))

# Finally, you can roll a different number of dice:
print("Roll 4 dice (always d6 in Traveller) %s" % Traveller.roll(dice=4))

# or this way:  (BUG HERE)
#print("Roll 4 dice (always d6 in Traveller) %s" % Traveller.roll(4))



# remember, you can always pass in debug=True to see more about what is happening
print("Roll 8+ on 2 dice %s" % Traveller.roll(target='8+', debug=True))