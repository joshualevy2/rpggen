
# Overview of the Rpggen Python Code

# Project List

If you would like to help out develop this library further, then please take a look at the following list of projects, or dream up your own:
1. Create a new "Generator" program.  Right now I have "YoungThugs" to create 16-24 year thugs, but that is about it.  
2. Add classes for more careers.  I have CorporateRepo, but that is it.
3. Add sample server code that works with Flask, Django, or your famorite web server framework.
3. Add classes for more Traveller rules varients.

Projects which are always helpful:
1. Make sure this library works with different versions of Python and on different machines.  I test mostly on Windows 10, running Python 3.5, so if you've got a mac, Linux, etc. please test there.
2. Extend the test suite.  I tend to add new tests when I'm adding a new feature, but it would help if someone added more tests to see how those features interacted, and to systematically test every dark corner of a feature.

# Quick Overview of Architecture (Objects and Layers)

There are three "layers":
1. The basic RPG layer, which is Rpggen, Table, Dice, Select, and Template (and uses Row "underneath"), and includes a json representations of Table, Dice, and Templates.
2. The Traveller layer, which is Traveller, and CepheusEngine.
3. Some higher level code, to create REST servers, etc.

In this library, there are often two or more different ways to do common things.  Some people really hate that, but I'm doing it to experiment with different interfaces. For example:
* "use" and "roll" often do the same thing.
* There is often a Rpggen way of doing something, and a more object oriented way of doing the same thing.
* Common objects (like dice, tables, etc.) can often be created via object creation or via json strings.

## RPG Layer

### Rolling Dice

   Rpggen.roll("2d10")
   Rpggen.use("1d6+2")
   d = Dice("3o4d6")
   d.use()
   d.roll()

The "d" means dice, as you would expect, and you can have possitive or negative adjustments at the end.  You can also roll dice that don't exist, like this "3d5" or "d17".  As you would expect, "1d4" is the same as "d4"

The "o" means "of" so you can roll "2o3d6" meaning roll three d6 but return the sum of the two best.

### Rolling on a Table

Simple tables are pretty much just lists:
    tab = Table("career", ["army", "navy", "marines", "scouts"])
    tab.use()
    tab.roll()

But you can also have more complex tables:
    tab2 = Table("home", {})
    tab.use()
    tab.roll()

### Templates

### Selections

## Traveller Layer

The idea is that the Traveller class includes "generic" Traveller rules, while the CepheusEngine class contains the rules specific to that system.  CepheusEngine inherits from Traveller.

However, the division between these two classes is poorly done at the moment.

Note that Traveller interprets numbers as d6, and can include a target roll:
   # Roll 1d6 and 2d6, respectively
   print("Roll 1 dice: %d" % Traveller.roll(1))
   print("Roll 2 dice: %d" % Traveller.roll(2))

   # All of these roll 2d6, which is the default Traveller roll.  Because a target is given,
   # the return boolean (True or False).
   print("Roll 8+ on 2 dice %s" % Traveller.roll(2, '8+'))
   print("Roll 10- on 2 dice %s" % Traveller.roll(2, '10-'))
   print("Roll 8+ on 2 dice %s" % Traveller.roll('8+'))
   print("Roll 10- on 2 dice %s" % Traveller.roll('10-'))
   print("Roll exactly 7 on 2 dice %s" % Traveller.roll('7'))

As another example of the difference.  The Traveller "Career" object will give a character two skills at one when they start a career for the first time.  While the CepheusEngine Career will give a character six skills at zero at the same point, because the rules are different.

## Other Useful Code

### REST Servers

In the samples directory are two python REST servers (simpleServer.py and youngThugServer.py).  They are both built on top of the Bottle framework.


# Quick Example of Writing A Program

# Quick Example of A Server