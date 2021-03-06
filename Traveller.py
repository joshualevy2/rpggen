
# Traveller.py

import logging
import random
import re

from GetFromWeb import GetFromWeb
from Rpggen import Rpggen, Table

class Attribute():
   '''This class is used to represent anything that has a level, although right now it is only 
      used for skills.  It is basically a tripple (name,level,cost).  However cost is

      name: the name of the attribute, skill, etc.
      value: the level of the attribute
      cost: (optional) Only used in character design schemes, this is the number of points
            needed to get this attribute to this level.

      This class has one global variable:
      useCost: a bollean to determine if cost should be used or not.      

      TODO: move dm() here?      
   '''
   useCost = False

   def __init__(self,name,value=None,cost=0):
      self.specific = None
      if '(' in name:
         parts = re.split('[()]', name)
         self.name = parts[0].strip()
         self.specific = parts[1].strip()
         if self.specific == '':
            raise ValueError('When creating Attribute(%s,...) specific skill was empty.' % name)
      else:
         self.name = name
      self.value = value
      #print('DEBUG (%s,%s) -> [%s|%s|%s]' % (name, value, self.name, self.specific, self.value))
      if self.useCost:
         self.cost = cost

   def fullName(self):
      if self.specific is None:
         return self.name
      else:
         return '%s(%s)' % (self.name,self.specific)

   def strAttr(self):
      specific = ''
      if self.specific is not None:
         specific = ' (%s)' % self.specific
      cost = ''
      if Attribute.useCost:
         cost = ' [%d]' % self.cost
      return '%s%s-%s%s' % (self.name, specific, self.value, cost)

class Career():
   '''This class represents one Traveller career.
      It mostly contains functions aimed at a character's pregression through that career.

      More specific rules (such as CepheusEngine or MegaTraveller) will have their own career
      classes which will usually inherit from this one.

      Also, each specific career (Scout, Army, Pirate, etc.) will inherit from this class.
   '''

   whichAdvantage = Table("WhichAdvantage",
                          ['MaterialBenefits','CashBenefits','PersonalDevelopment',
                           'ServiceDevelopment'])

   def __init__(self,config):
      try:
         self.name = config['name']
         self.config = config
         self.log = []
      except:
         raise ValueError('Config did not have the items required.')

   def addData(self,name,data):
      self.config[name] = data

   # TODO remove this? use addData+Table
   def addTable(self,name,tab=None):
      '''Add this table to the career creation system.
         If two areguments are passed in, use the first as the name.
         Otherwise, use the table's id as the name.
      '''
      if tab is None:
         tab = name
         name = tab.id
      self.config[name] = tab

   def changeName(self,name):
      self.name = name
      self.config['name'] = name  

   def doBasicTraining(self, character):
      # TODO put in seperate function
      character.history.append('In basic training')
      which = self.whichAdvantage.use()
      adv = Rpggen.finduse(which)
      character.changeStr(adv)

   def doMusteringOut(self, character):
     # CE31
     # Calculate pension
     if character.rank > 4:
        character.money['pension'] = 2000 * character.rank
        character.history.append('Got a pension of %d' % character.money['pension'])

     # Calculate number of benefits
     benefitCount = character.terms
     if character.rank >= 4:
        benefitCount = character.rank - 2
     # Divide between cash and material
     cashBenefits = 0
     materialBenefits = 0
     if benefitCount < 3:
        cashBenefits = benefitCount
     elif 3 <= benefitCount:
        cashBenefits = 2
        materialBenefits = benefitCount - 2

     character.history.append('Ended up with %d cash and %d material benefits' %
                              (cashBenefits, materialBenefits))
     for num in range(cashBenefits):
        benefit = Rpggen.finduse('CashBenefits')
        character.money['bank'] += Traveller.str2cr(benefit)
        character.history.append(benefit)
     for num in range(materialBenefits):
        benefit = Rpggen.finduse('MaterialBenefits')
        if benefit.startswith('+'):
           character.changeStr(benefit)
        else:
           character.possessions.append(benefit)
        character.history.append(benefit)

   def doOneTerm(self, character, debug=False):
      '''Adds one term to a character.
         Returns None if the career continues, or a string if the career
         ends, the string stating why the career ends.
      '''
      if debug:
         print('entering doOneTerm')
      character.history.append('Starting a new term.')
      if character.terms == 7:
         result = 'Aged out of career.'
         character.history.append(result)
         return result
      if not character.checkStr(self.config['survival']):
         result = 'Did not survive.'
         character.history.append(result)
         return result
      character.terms += 1
      character.age += 4

      # TODO use funciton here
      which = self.whichAdvantage.use()
      adv = Rpggen.finduse(which)
      character.changeStr(adv)

      print('rank %d' % character.rank)
      if character.rank == 0:
         print('foo')
         if character.checkStr(self.config['commission']):
            character.history.append('Was commissioned')
            character.rank = 1
            newSkill = self.config['Skills'][character.rank-1]
            if newSkill is not None:
               character.changeStr(newSkill)
      else:
         if character.checkStr(self.config['advancement']):
            character.history.append('Advanced in rank.')
            character.rank += 1
            newSkill = self.config['Skills'][character.rank-1]
            if newSkill is not None:
               character.changeStr(newSkill)

      if self.roll('reenlistment'):
         return 'Could not reenlist.'

      return None

   def roll(self, name):
      '''Roll on the named item for this career.
         Only works on rolls specific to a career (reenlistment, survival, etc.)
         Returnes True if succeeds and False if it fails.
         Raises an exception if the argument is not known to this career.
      '''
      try:
         target = self.config[name]
      except:
         KeyError('The Career %s did not have a config item called %s' % (self.name, name))
      return Traveller.roll(target=target)

   def use(self, name):
      '''Roll on the named item for this career.
         Returnes True if succeeds and False if it fails.
         Raises an exception if the argument is not known to this career.
      '''
      try:
         tab = self.config[name]
      except:
         KeyError('The Career %s did not have a config item called %s' % (self.name, name))
      return tab.use()

   def printTestHelper(self, name):
      try:
        data = self.config[name]
        print('Has %s: %s' % (name, str(data)))
      except KeyError:
        print('Does not have %s.' % name)

   def printTest(self):
      self.printTestHelper('name')
      self.printTestHelper('qualifications')
      self.printTestHelper('survival')
      self.printTestHelper('commission')
      self.printTestHelper('advancement')
      self.printTestHelper('reenlistment')
      self.printTestHelper('Ranks')
      self.printTestHelper('Skills')
      self.printTestHelper('MaterialBenefits')
      self.printTestHelper('CashBenefits')
      self.printTestHelper('PersonalDevelopment')
      self.printTestHelper('ServiceDevelopment')
      self.printTestHelper('SpecialistDevelopment')
      self.printTestHelper('AdvancedDevelopment')

class Character():
   '''This class represents a character in Traveller.

      More specific rules may want to subclass it, if they have more attributes.
   '''

   attrShort = ['dex','end','int','edu','str','soc','psi']

   def __init__(self):
      self.name = ''
      self.lastCareer = ''
      self.terms = -1
      self.age = -1
      self.str = -1
      self.dex = -1
      self.end = -1
      self.int = -1
      self.edu = -1
      self.soc = -1
      self.psi = None
      self.rank = 0
      self.skills = []
      self.equipment = []
      self.money = { 'pocket': 0, 'bank': 0, 'pension': 0}
      self.possessions  = []
      self.history = []

#   def internalCheck(self):
#      if

   def addToSkill(self, name, specific, value=None):
      # TODO: do we need this?
      if value is None:
         value = specific
         specific = None
      exists = False   
      for skill in self.skills:
         if name == skill.name and specific == skill.specific:
            skill.value += value
            exists = True
      if not exists:
         # TODO: doesn't support specific
         self.skills.append(Attribute(name,value))

   def availableMoney(self):
      '''Returns the common amount of money (pocket+bank but not pension)'''
      pocket = self.money['pocket']
      bank = self.money['bank']
      return pocket + bank

   def createUpToCareer(self):
      self.history.append('Birth')
      self.name = GetFromWeb.get('names')
      self.lastCareer = "No Career"
      self.terms = 0
      self.age = 18
      self.str = Rpggen.roll('2d6')
      self.dex = Rpggen.roll('2d6')
      self.end = Rpggen.roll('2d6')
      self.int = Rpggen.roll('2d6')
      self.edu = Rpggen.roll('2d6')
      self.soc = Rpggen.roll('2d6')

   def createUsingTimeline(self, career=None, debug=False):
      # Do all the pre-career character generation steps.

      if career is None:
         raise ValueError('TODO: must provide a career.')

      self.createUpToCareer()
      self.lastCareer = 'Corporate Repo'
 
      # Do basic training for this person
      career.doBasicTraining(self)

      endReason = None 
      while endReason is None:
         endReason = career.doOneTerm(self, debug=False)

      self.endReason = endReason
      self.history.append(endReason)
      career.doMusteringOut(self)

   def dict(self):
      '''Returns the character in dictionary format
      '''
      # TODO: need to review/improve this?
      return self.__dict__

   def dm(self, attr):
      attr = attr.lower()
      if attr == 'dex': return Traveller.dm(self.dex)
      if attr == 'end': return Traveller.dm(self.end)
      if attr == 'int': return Traveller.dm(self.int)
      if attr == 'edu': return Traveller.dm(self.edu)
      if attr == 'str': return Traveller.dm(self.str)
      if attr == 'soc': return Traveller.dm(self.soc)
      if attr == 'psi': return Traveller.dm(self.psi)


   def getSkill(self, name):
      for skill in self.skills:
         if skill.fullName() == name:
            return skill
      return None

   def roll(self, attr, target, debug=False):
      dm = self.dm(attr)
      result = Traveller.roll(target=target, dm=dm)
      if debug:
         print('in Character roll: attr=%s target=%s dm=%s' %
               (attr, target, dm))
      return result

   def skillNames(self):
      skillNames = []
      for skill in self.skills:
         skillNames.append(skill.name)
      return skillNames

   def strHistory(self):
      '''Returns a character's history as a string.
      '''
      result = 'History:\n'
      for history in self.history:
         result += history+'\n'
      return result

   def strSmall(self):
      '''Returns a character's characteristics as a string (a mini-character sheet).
      '''      
      result = ''
      result += ('Name: %s --- %s --- %d years old\n' %
                 (self.name, self.strUpp(),self.age))
      result += ('%s (%d term%s) ended up with rank of %d    Cr%d\n' %
                 (self.strCareer(), self.terms, ("s" if (self.terms!=1) else ""),
                  self.rank,
                  self.availableMoney()))
      result += '\n'
      result += self.strSkills()+'\n'
      result += 'Equipment: %s\n' % ', '.join(self.equipment)
      result += ('Money: %d in pocket, %d in bank, %d in pension\n' %
                 (self.money['pocket'], self.money['bank'], self.money['pension']))
      if len(self.possessions) > 0:
         result += 'Possesions: %s\n' % ', '.join(self.possessions)
      result += '\n'
      return result

   def strCareer(self):
      if self.lastCareer == None:
         return ''
      return self.lastCareer

   def strSkills(self):
      result = ''
      for skill in self.skills:
          if result != '':
              result += ', '
          result += skill.strAttr()
      return "Skills: "+result

   def strUpp(self):
      '''Returns the character's Universal Person Profile as a string.
      '''
      base = (Traveller.digit2char(self.str)+Traveller.digit2char(self.dex)+
              Traveller.digit2char(self.end)+Traveller.digit2char(self.int)+
              Traveller.digit2char(self.edu)+Traveller.digit2char(self.soc))
      if self.psi is not None:
         base += "-"+Traveller.digit2char(self.psi)
      return base

class Profile():
   id = None
   letters = []
   extras = []
   rules = {}
   value = ''

   Attr = '23456789AB'
   Hex = '123456789ABCDEF'
   Starports = 'ABCDEX'


   def __init__(self, name, letters, extras=None, format=None, rules=None):
      self.id = name
      self.format = format
      self.letters = letters
      self.extras = extras
      self.rules = rules

   def generate(self):
      result = ''
      for letter in self.letters:
          result = '%s%s' % (result,random.choice(letter))
      self.value = result
      return self.value

   def smallStr(self):
      if self.format is not None:
         return self.format % tuple(self.value)
      else:
         result = ''
         if self.value == '':
            return result
         for letter in self.value:
            result = '%s%s' % (result,letter)
         return result


class Traveller():

   majorRaces = [ 'Vlandi', 'Solomani', 'Vargr', 'Aslan']
   minorRaces = [ 'Hhakr', 'Vegan']
   races = majorRaces + minorRaces

   customziations = {}
   Rpggen.setCustomization('d66support',True)

   @classmethod
   def digit2char(cls,num):
      """This function takes a number (usually one digit) and converts it to
         a hex digit (0-F).  Letters are upper case.
         TODO: make it work for non-standard digit conversion
      """
      return hex(num)[2].upper()

   @classmethod
   def dm(cls,num):
      """
      """
      return 0

   @classmethod
   def iscr(cls, str):
      try:
         match = re.search(r"^(\$|[Cc][Rr] ?)?([0123456789]+)$", str)
         result = int(match.group(2))
         return True
      except:
         return False         

   @classmethod
   def str2cr(cls, str):
      match = re.search(r"^(\$|[Cc][Rr] ?)?([0123456789]+)$", str)
      return int(match.group(2))   

   # Since traveller implies 2d6 most of the time, the default string passed is the
   # target, not the dice roll, and the dice modifier comes second.
   @classmethod
   def roll(cls, target=None, dm=None, dice=None, debug=False):
      if debug:
         print('roll(%s, %s, %s)' % (dice,target,dm))
      got = Rpggen.roll("2d6")
      if dice is not None:
         if type(dice) == int:
            got = Rpggen.roll(str(dice)+"d6")
         if type(dice) == str:
            got = Rpggen.roll(dice)

      if debug:      
         logging.debug('raw roll %d' % got)
      dmValue = 0
      if dm is not None:
       if type(dm) == int:
         got = got + dm
       if type(dm) == str:
         dmMatch = re.search(r"^([+-]?)([0123456789]+)$", dm)
         dmDir = dmMatch.group(1)
         if dmDir is None: dmDir = '+'
         dmValue = int(dmMatch.group(2))
         if dmDir == '+':
            got = got + dmValue
         elif dmDir == '-':
            got = got - dmValue

      if target is None:
          #print('returning %d' % got)
          return got

      targetMatch = re.search(r"^([0123456789]+)([+-]?)$", target)
      #print(targetMatch)
      if targetMatch is None:
         raise ValueError('In Traveller.roll(), target of %s matched noting' % target)


      targetNum = int(targetMatch.group(1))
      targetCmp = targetMatch.group(2)
      if debug:
         print('%s %d %d' % (targetCmp, got, targetNum))      
      if targetCmp is None:
         return got == targetNum
      elif targetCmp == '+':
         return got >= targetNum
      elif targetCmp == '-':
         return got <= targetNum
      else:
         raise ValueError('In roll(), target string (%s) is malformed.' % target)

   def setAllCustomizations(self,customizations):
      '''Sets all customizations by replacing whatever is there with those listed
         in the argument.  Previous customizations are lost, even if their is non-standard
         similar customization in the argument.
      '''
      self.customziations = customizations

   def setCustomization(self, name, value):
      '''Sets one customization.  Either changes the value, if it already exists,
         or creates it new, with the given value.
      '''
      self.customziations[name] = value

   def getCustomization(self, name, default=None):
      '''Returns the customization value, or the second argument, if that
         customization is not set, or None if the second argument is empty.
      '''
      if customizations is None:
         return default
      try:
         result = self.customizations[name]
         return result
      except KeyError:
         return default

if __name__ == '__main__':
   print('Test Traveller Code:')
   print("Roll 1 dice: %d" % Traveller.roll(1))
   print("Roll 2 dice: %d" % Traveller.roll(2))

   print("Roll 8+ on 2 dice %s" % Traveller.roll(2, '8+'))
   print("Roll 10+ on 2 dice %s" % Traveller.roll(2, '10+'))
   print("Roll 8+ on 2 dice %s" % Traveller.roll('8+'))
   print("Roll 10+ on 2 dice %s" % Traveller.roll('10+'))

   print("Roll 13+ on 2 dice %s" % Traveller.roll(2, '13+'))
   print("Roll 13+ on 2 dice %s" % Traveller.roll(2, '13+'))
   print("Roll 13+ on 2 dice %s" % Traveller.roll('13+'))
   print("Roll 13+ on 2 dice %s" % Traveller.roll('13+'))

   print("Roll 1+ on 2 dice %s" % Traveller.roll(2, '1+'))
   print("Roll 1+ on 2 dice %s" % Traveller.roll(2, '1+'))
   print("Roll 1+ on 2 dice %s" % Traveller.roll('1+'))
   print("Roll 1+ on 2 dice %s" % Traveller.roll('1+'))
