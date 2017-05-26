
# This python program is BOTH a program you can run, and tutorial you can read.
# The code runs, and the comments are the tutorial.
#
# This file covers the basic Rpggen library.
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

# Rule 1: In almost all cases, there is more than one way to do anything
# important.  My philosphy is that there should be different ways of doing
# each thing, so that we can all see which is best (and under what
# circomestances).  The first application of Rule 1, is that most functionality
# can be used both from the Rpggen class itself, and by more specific classes
# such as Dice, Table, etc.

# Dice work the way that role players expect:

# You can roll dice from Rpggen:
print(Rpggen.use("3d6"))
# Or by using dice:
dice = Dice("1d10+3")
print(dice.roll())

# Rule 1(b): All objects have a method called "use", which uses that object,
# but many of the object also have a method called "roll" which does the same
# thing.  Because sometimes it just feels better to sa "use" and other times it 
# feels better to say "roll".

print(dice.use())

# Rpggen also supports Tables.
# You can create tables in three different ways, and I'll go through each one
# in turn, and the discuss which type of table you should use in which
# situation.

tab1 = Table('PlanetaryOcean', ['On Surface', 'Under A Thin Crust', 'Deep Underground'])

tab2 = Table('Race', { '1-3': 'Human', '4-5': "Elf", '6': 'Dwarf'})

# and you can use these tables in the obvious ways:
print(tab1.use())
print(tab2.roll())

# Rule 2: many functions support a "debug=True" option.  If you pass that
# option in, it will print out debugging information designed to help you
# figure out what is going on, and why it is happening.

# You can also do several other interesting things with tables:

# Get a list of all possible results:

# Set the dice that will be used, and get that later:

tab3 = Table('Race', { 'roll': '2d4', 
             '2-5': 'Human', '6': "Elf", '7': 'Dwarf', '8': 'Halfling'})
print(tab3.dice)
print(tab3.results())

# A second way to create a table is by reading in an "lt" file.
# This is a file formatting in the following way:
# Lines that start with '#' are ignored.
# Each other line is one result from the table.
# Each result has an equal chance of occuring.

# First you read the file

tab4 = Rpggen.loadLt('simple.lt')
print('Just read in table %s, and use it once: %s' % (tab4.id, tab4.use()))

# Why use an lt file?
# **

# A third way to create tables is by creating a json file which contains 
# several tables, which are all loaded together.

Rpggen.load('simple.json')

# If you've never written json files before, here is an ultra quick introduction.
# But you can read a lot more on the web.
# The Rpggen library uses jsoncomment to read json files, so it understand 
# basic json plus comments, and that is it:
# Comments start with a # and go to the end of the line.
# The file is a list of dictionaries.
# A list is enclosed in [ ]
# A dictionary is enclosed in { }
#

# In order to use the tables in the json file, you need to find them, using their id.
# This is done as follows:

tab5 = Rpggen.find('SimpleTableInJson')
print('Using table %s gives result: %s' % ('SimpleTableInJson', tab5.use()))

# Or you can do both the find and the use at once:
result5 = Rpggen.finduse('SimpleTableInJson')
print('Using table %s gives result: %s' % ('SimpleTableInJson', result5))

# Rolling Uniquely

# When you roll normally on a table, you can get the same results many times:

print('Normally you can get the same result over and over again:')
for ii in range(10):
   print(tab3.use()+' ', end='')
print('')

# But what if you want all roles to be unique?  Then you set the table to "unique":

print('But **')
tab3.unique(True)
try:
   for ii in range(10):
      print(tab3.use()+' ', end='')
except ValueError:
   print('')
   print('Caught a ValueError to signal all rows of the table have been used.')


# **

tab3.unique(False)
print('Now you can get the same result over and over again:')
for ii in range(10):
   print(tab3.use()+' ', end='')
print('')
