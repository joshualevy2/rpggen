
from GetFromWeb import GetFromWeb
import logging
import re
from Rpggen import Table, Rpggen
from Traveller import Attribute, Career, Character, Traveller

class CepheusEngine():

   def __init__(self):
      return
            
class Character(Character):
   '''This Class represents a CepheusEngine specific Character.
      Because it inherits from Traveller.Character, the only code here should be differences
      from Traveller.  (Different lists of skills, for example.)
   '''

   skills = [ 'Admin','GunCombat(CascadeSkill)','Vehicle(CascadeSkill)','Advocate',
              'Archery',
              'Aircraft (CascadeSkill)','Animals (CascadeSkill)','EnergyPistol',
              'GravVehicle','Farming','Energy Rifle','RotorAircraft','Riding',
              'Shotgun','Winged Aircraft','Survival','SlugPistol','Mole',
              'Veterinary Medicine','SlugRifle','TrackedVehicle','Athletics',
              'Gunnery(CascadeSkill)','Watercraft (CascadeSkill)','BattleDress',
              'Bay Weapons','Motorboats','Bribery','HeavyWeapons','OceanShips',
              'Broker', 'Screens', 'Sailing Ships', 'Carousing', 'SpinalMounts',
              'Submarine', 'Comms', 'Turret Weapons', 'Wheeled Vehicle', 'Computer',
              'MeleeCombat(CascadeSkill)', 'Demolitions', 'BludgeoningWeapons',
              'Electronics', 'NaturalWeapons', 'Engineering', 'Piercing Weapons',
              'Gambling', 'SlashingWeapons', 'Gravitics', 'Jack-of-All-Trades',
              'Leadership', 'Linguistics', 'Liaison', 'Mechanics', 'Medicine',
              'Navigation', 'Piloting', 'Recon', 'Sciences(CascadeSkill)', 'LifeSciences',
              'PhysicalSciences', 'SocialSciences', 'SpaceSciences', 'Steward',
              'Streetwise','Tactics', 'Zero-G']

   skillTab = None 

   def __init__(self):
      super().__init__()
      if Character.skillTab is None:
         Character.skillTab = Table('skills', Character.skills)
      
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
      self.history.append('At 18 has: %s' % self.strUpp())

   def createRandomlyTopdown(self):
       self.history.append('--> Using Topdown randomly')
       self.createUpToCareer()
       self.terms = Rpggen.roll('1d7')
       self.age = 18 + self.terms*4
       self.lastCareer = 'Corporate Repo'
       if self.terms == 1:
           numSkills = 3
       elif self.terms == 2:
           numSkills = 5
       else:
           numSkills = (self.terms-1)*2 + Rpggen.roll('2d2')
       for nSkill in range(numSkills):
           skillLevel = Rpggen.roll('1d4-1')
           skillName = Rpggen.finduse("skills")
           self.skills.append(Attribute(skillName, skillLevel))

   def changeStr(self, command):
      logging.debug('changeStr(%s)' % str(command))
      self.history.append(command)
      if type(command) == list:
         raise ValueError('For changeCharacter, command can not be a list (yet).')
      parts = command.split(' ')
      logging.debug('In changeStr: %s' % "|".join(parts))
      if len(parts) == 1:
         self.change(('skill', parts[0], 'add', '1')) 
      elif len(parts) ==2:
         # ''+1 Dex' -> 'attr, dex, add 1'
         if parts[1].lower() in Character.attrShort:
            self.change(('attr', parts[1], 'add', str(parts[0])))

         # '10' , '$10', 'cr10' -> money onhand add 10
         if parts[1][0] == '$' or parts[1][0:1].lower() == "cr":
            self.change(('money', parts[1], 'add', str(parts[0])))

                       

   def change(self, command):
      logging.debug('Changing %s for %s' % ("|".join(command),self.name))
      if type(command) == list:
         raise ValueError('For changeCharacter, command can not be a list (yet).')
      if command[0] == "attr":
         if command[1].lower() == "str":
            if command[2] == "add":
               self.str += int(command[3])
         if command[1].lower() == "dex":
            if command[2] == "add":
               self.dex += int(command[3])
         if command[1].lower() == "end":
            if command[2] == "add":
               self.end += int(command[3])
         if command[1].lower() == "int":
            if command[2] == "add":
               self.int += int(command[3])
         if command[1].lower() == "edu":
            if command[2] == "add":
               self.edu += int(command[3])
         if command[1].lower() == "soc":
            if command[2] == "add":
               self.soc += int(command[3])
         if command[1].lower() == "psi":
            if command[2] == "add":
               self.psi += int(command[3])
      elif command[0] == "skill":
         attr = self.getSkill(command[1])
         if attr is None:
            self.skills.append(Attribute(command[1],1))
         else:
            attr.value += 1
      elif command[0] == "money":
         a = 0
      elif command[0] == "stuff":
         if command[1] == "add":
           self.equipment.append(command[2])
         else:
           print('Could not change %s for %s' % (command,self.name))

   def checkStr(self,command):
      '''This function implmenents attribute checks on a character.
         Sample call: character.checkStr('int 8+')
         TODO: In the future, it will do skills as well.
      '''
      parsed = command.split(' ')
      result = Traveller.roll(dm=Traveller.dm(parsed[0]), target=parsed[1]) 
      return result

   def doBasicTraining(self, character):
      self.history.append('In basic training')
      for skill in self.config['ServiceDevelopment'].results():
         character.changeStr(skill) 

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
