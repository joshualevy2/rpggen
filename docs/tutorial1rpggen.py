
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
print('Rolling on 3d6: %s' % Rpggen.use("3d6"))
# Or by using dice:
dice = Dice("1d10+3")
print('Rolling on 1d10+3: %s' % dice.roll())

# Note that rolling dice currently returns a string.

# Rule 1(b): All objects have a method called "use", which uses that object,
# but many of the object also have a method called "roll" which does the same
# thing.  Because sometimes it just feels better to sa "use" and other times it 
# feels better to say "roll".

print('Rolling 1d10+3 again: %s' % dice.use())

# Rpggen also supports Tables.
# You can create tables in three different ways, and I'll go through each one
# in turn, and the discuss which type of table you should use in which
# situation.

tab1 = Table('PlanetaryOcean', ['On Surface', 'Under A Thin Crust', 'Deep Underground'])

tab2 = Table('Race', { '1-3': 'Human', '4-5': "Elf", '6': 'Dwarf'})

# and you can use these tables in the obvious ways:
print('Using the PlanetaryOcean table: %s' % tab1.use())
print('Using the Race table: %s' % tab2.roll())

# Rule 2: many functions support a "debug=True" option.  If you pass that
# option in, it will print out debugging information designed to help you
# figure out what is going on, and why it is happening.

# You can also do several other interesting things with tables:

# Get a list of all possible results:
# TBD

# Set the dice that will be used, and get that later:

tab3 = Table('Race', { 'roll': '2d4', 
             '2-5': 'Human', '6': "Elf", '7': 'Dwarf', '8': 'Halfling'})
print('Print the dice roll used in the second Race table: %s' % tab3.dice)
print('And print out all possible results from that table: %s' % tab3.results())

# A second way to create a table is by reading in an "lt" file.
# This is a file formatting in the following way:
# Lines that start with '#' are ignored.
# Each other line is one result from the table.
# Each result has an equal chance of occuring.

# First you read the file

tab4 = Rpggen.loadLt('simple.lt')
print('Use the table in file simple.lt: %s' % tab4.use())

# Why use an lt file?
# TBD

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

# TBD print('But **')
# TBD tab3.unique(True)
# TBD try:
# TBD    for ii in range(10):
# TBD       print(tab3.use()+' ', end='')
# TBD except ValueError:
# TBD    print('')
# TBD    print('Caught a ValueError to signal all rows of the table have been used.')


# **

# TBD tab3.unique(False)
# TBD print('Now you can get the same result over and over again:')
# TBD for ii in range(10):
# TBD    print(tab3.use()+' ', end='')
# TBD print('')

# Now on to templates.

# TBD

# Finally, sometimes you just want to choose randomly from a list:

res1 = Select.choose(['one','two','three','four'])
print('Selected one string from four: %s' % res1)

# And lastly, you often need to test your work!

# To help you do that, if Rpggen.testData is set, then all dice will end up 
# rolling that number, and all tables will return the same piece of data.

Rpggen.testData = 6
d6 = Dice('d6')
print('With Rpggen.testData set to 6, 1d6 is always 6: ', end='')
for ii in range(10):
   print(str(d6.use())+' ', end='')
print('')

d62 = Dice('2d6')
print('And 2d6 is always 12: ', end='')
for ii in range(10):
   print(str(d62.use())+' ', end='')
print('')

print('And a table will always react as though you rolled 6: ')
for ii in range(10):
   print(tab2.use()+' ', end='')
print('')

# And you can change the forced roll later (over and over, if you want to test
# different situations).

Rpggen.testData = 3
print('Now Rpggen.testData is set to 3, so 1d6 is always 3: ', end='')
for ii in range(10):
   print(str(d6.use())+' ', end='')
print('')