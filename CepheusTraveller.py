
from GetFromWeb import GetFromWeb
import re
from rpggen import Table, Rpggen
from Traveller import Attribute, Career, Character, Traveller

class CepheusTraveller():

   law2combat = { 
    "No Law" : "Gun Combat-0",
    "Low Law" : "Gun Combat-0",
    "Medium Law" : "Gun Combat-0",
    "High Law" : "Melee Combat-0"
   }
   
   trade2skill = { 
    "1" : "rock.",
    "2" : "boulders.",
    "3" : "rock with some dust.",
    "4" : "boulders with some dust.",
    "5" : "rock core with ice and dust on the outside."
   }

   def __init__(self):
      #Rpggen.load("CepheusTraveller.rpggen")
      return
       
class CorporateRepo(Career):
   name = 'Corporate Repo'
   
   @classmethod
   def setup(self):
      #Rpggen.load('CorporateRepo.rpggen')
      pass
      
   def doBasicTraining(self, char):
      char.change(('skill','add','Liaison', '0'))
      
class Character(Character):

   skills = [ 'Admin','Gun Combat (Cascade Skill)','Vehicle (Cascade Skill)','Advocate',
              'Archery',
              'Aircraft (Cascade Skill)','Animals (Cascade Skill)','Energy Pistol',
              'Grav Vehicle','Farming','Energy Rifle','Rotor Aircraft','Riding',
              'Shotgun','Winged Aircraft','Survival','Slug Pistol','Mole',
              'Veterinary Medicine','Slug Rifle','Tracked Vehicle','Athletics',
              'Gunnery (Cascade Skill)','Watercraft (Cascade Skill)','Battle Dress',
              'Bay Weapons','Motorboats','Bribery','Heavy Weapons','Ocean Ships',
              'Broker', 'Screens', 'Sailing Ships', 'Carousing', 'Spinal Mounts',
              'Submarine', 'Comms', 'Turret Weapons', 'Wheeled Vehicle', 'Computer',
              'Melee Combat (Cascade Skill)', 'Demolitions', 'Bludgeoning Weapons',
              'Electronics', 'Natural Weapons', 'Engineering', 'Piercing Weapons',
              'Gambling', 'Slashing Weapons', 'Gravitics', 'Jack-of-All-Trades',
              'Leadership', 'Linguistics', 'Liaison', 'Mechanics', 'Medicine',
              'Navigation', 'Piloting', 'Recon', 'Sciences (Cascade Skill)', 'Life Sciences',
              'Physical Sciences', 'Social Sciences', 'Space Sciences', 'Steward',
              'Streetwise', 'Tactics', 'Zero-G']

   skillTab = Table('skills', skills)

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
      self.skills = []
      self.equipment = []
      self.money = { 'pocket': 0, 'bank': 0, 'pension': 0}
      self.history = []
      
   def createUpToCareer(self):
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

   def createRandomlyTopdown(self):
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

   def changeStr(command):
        if type(command) == list:
            raise ValueError('For changeCharacter, command can not be a list (yet).')
        parts = command.split(' ')
        print('In changeEnglish: %s' % parts)
        # ''+1 Dex' -> 'attr, dex, add 1'
        if parts[1].lower() in Traveller.attrShort:
            change(('attr', parts[1], 'add', str(parts[0])))

        # '10' , '$10', 'cr10' -> money onhand add 10
        if parts[1][0] == '$' or parts[1][0:1].lower() == "cr":
            change(('money', parts[1], 'add', str(parts[0])))

        if parts[1] in skills:
            change(('skill', parts[0], 'add', '1'))            

   def change(self,command):
      print('Changing %s for %s' % (command,self.name))
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
         a = 0
      elif command[0] == "money":
         a = 0
      elif command[0] == "stuff":
         if command[1] == "add":
           self.equipment.append(command[2])
         else:
           print('Could not change %s for %s' % (command,self.name))

   def checkStr(command):
       parsed = command.split(' ')
       Traveller.roll() 

   def doBasicTraining(self, character):
      for skill in self.config['ServiceDevelopment'].results():
         character.skills.append(Attribute(skill,1)) 

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
