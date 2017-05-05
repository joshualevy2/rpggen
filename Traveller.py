
from GetFromWeb import GetFromWeb
import random
import re
from rpggen import Rpggen, Table

class Attribute():

   useCost = False

   def __init__(self,name,value=None,cost=0):
      self.name = name
      self.value = value
      self.cost = cost

   def strAttr(self):
       if Attribute.useCost:
          return '%s-%s [%d]' % (self.name, self.value, self.cost)
       else:
          return '%s-%s' % (self.name, self.value)

class Career():
   #name = ''
   #config = {}

   def __init__(self,config):
      try:
         self.name = config['name']
         self.config = config
         self.log = []
         self.history = []
      except:
         raise ValueError('Config did not have the items required.') 

   def addData(self,name,data):
      self.config[name] = data

   def addTable(self,name,data):
      self.config[name] = Table(data)

   def changeName(self,name):
      self.name = name
      self.config['name'] = name

   def doBasicTraining(self, character):
      for skill in self.config['ServiceDevelopment'].results():
         character.skills.append(Attribute(skill,1))      

   def doOneTerm(self, character):
      '''Adds one term to a character.
         Returns None if the career continues, or a string if the career
         ends, the string stating why the career ends.
      '''
      mustEnd = None
      if character.terms == 7:
          return 'Aged out of career'
      character.terms += 1
      
      if self.roll('reenlistment'):
         return 'Could not reenlist.'
         
      return mustEnd

   def roll(self, name):
      '''Roll on the named item for this career.
         Returnes True if succeeds and False if it fails.
         Raises an exception if the argument is not known to this career.
      '''
      roll = self.config[name]
      return Traveller.roll(target=roll)
      
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

   def addToSkill(self, name, value):
      for skill in self.skills:
         if name == skill.name:
            skill.value += value
            
   def availableMoney(self):
      '''Returns the common amount of money (pocket+bank but not pension)'''
      pocket = self.money['pocket']
      bank = self.money['bank']
      return pocket + bank
   
   def dm(self, attr):
      if attr == 'dex': return Traveller.dm(self.dex)
      if attr == 'end': return Traveller.dm(self.end)
      if attr == 'int': return Traveller.dm(self.int)
      if attr == 'edu': return Traveller.dm(self.edu)
      if attr == 'str': return Traveller.dm(self.str)
      if attr == 'soc': return Traveller.dm(self.soc)
      if attr == 'psi': return Traveller.dm(self.psi)

   def roll(self, attr, target):
      return Traveller.roll(target=target, dm=self.dm(attr))
      
   def skillNames(self):
      skillNames = []
      for skill in self.skills:
         skillNames.append(skill.name)
      return skillNames

   def strSmall(self):
       print('Name: %s        %s  %d years old' % 
             (self.name, self.strUpp(),self.age))
       print('%s %d term%s              Cr%d' % (self.strCareer(), self.terms, ("s" if (self.terms!=1) else ""), self.availableMoney()))
       print('')
       print(self.strSkills())
       print('Equipment: '+str(self.equipment))
       print('Money: '+str(self.money))
       print('')

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

   customziations = {}
   
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
   def roll(cls, dice=None, target=None, dm=None):
      #print('roll(%s, %s, %s)' % (dice,target,dm))
      got = Rpggen.roll("2d6")
      if dice is not None:
         if type(dice) == int:
            got = Rpggen.roll(str(dice)+"d6")
         if type(dice) == str:
            got = Rpggen.roll(dice)

      #print('raw roll %d' % got)
      dmValue = 0
      if type(dm) == int:
         got = got + dm
      if dm is not None and type(dm) == str:
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
      
      targetNum = int(targetMatch.group(1))
      targetCmp = targetMatch.group(2)
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
