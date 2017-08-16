
# This file contains to to generate "Young Thugs", who are 16-22 years old criminals.
# In addition to doing something useful, it also serves as sample code to show you how
# to generate and display characters using this library.
#
# It is heavily commented, and the comments are designed to teach you why things are
# done the way they are done, and discuss options about other ways to do things.

import logging
import string
import sys
import json
from yattag import Doc

sys.path.append('..')
from CepheusEngine import Character
from GetFromWeb import GetFromWeb
from Rpggen import Rpggen, Select, Table
from Traveller import Attribute, Traveller

# TODO Why not CepheusEngine.Character?
class YoungThug(Character):
   # Updated when improvements are made to the generation algorithm.
   version = '0.1'

   # Tables are class variables, not object variables, so that when we print out the YoungThug
   # class as a json string, we do NOT include these tables.

   meleeSkills = Table("MeleeSkills", ['Melee Combat (Blugeoning)', 'Melee Combat (Piercing)',
		                                   'Melee Combat (Slashing)'], unique=True)
   weaponSkills = Table("WeaponsSkills",
                        ['Gun Combat (EnergyRifle)','Gun Combat (EnergyPistol)',
		                   'Gun Combat (Shotgun)', 'GunCombat (SlugRifle)',
		                   'Gun Combat (SlugPistol)'],
                        unique=True)

   otherSkills = Table("OtherSkills", 
                       ['Bribery', 'Courousing', 'Gambling', 'Leadership', 'Mechanics',
                        'Medicine', 'Recon', 'Streetwise', 'Tactics'],
		                 unique=True)
   # This is a very generic table, which should be overwritten by a better one in the
   # setting table
   possessionsTable = Table('PossessionsTable',
                            ['Key', 'Legal Drugs', 'Illegal Drugs', 'Gambling Materials',
                             'Gear Bag', 'Shades', 'Broken Jewlery', 
                             'Forgerly or Lockpicking Equipment', 'Jumk Food',
                             'Gloves', 'Flask', 'Photo', 'Torn Up Photo', 'Mints',
                             'Plastic Tie','Bandage(s) or BandAid(s)', 'Sanitizer',
                             'Lip Balm or Handcream'])
   personalityTable = Rpggen.loadLt("PersonalityTraits.lt") 

   def __init__(self):
      super().__init__()
      Rpggen.clear()
      try:
         Rpggen.load("Setting.rpggen")
      except:
         print('Warning: could not find data file Setting.rpggen.') 
         print(sys.exc_info()[1])    
     

   def generate(self, debug=False):
      '''Create a young thug.
      '''
      Rpggen.clear()
      self.name = GetFromWeb.get('names')
      self.name = string.capwords(self.name)
      if debug:
         print(self.name)
      self.lastCareer = "No Career"    
      self.str = Rpggen.roll('2d5+2')
      self.dex = Rpggen.roll('2d5+2')
      self.end = Rpggen.roll('2d5+2')
      self.int = Rpggen.roll('2d5')
      self.edu = Rpggen.roll('2d2')
      self.soc = Rpggen.roll('2d3')

      if YoungThug.personalityTable is not None:
         self.personality = YoungThug.personalityTable.rollRepeatedly(3, unique=True)

      level = Select.choose(['teen','start', 'young'])
      if level == 'teen':
         self.age = Rpggen.roll('1d3+15')
         self.terms = 0  
         numSkills = 2   # TODO right number?     
      elif level == 'start':
         self.age = Rpggen.roll('1d3+17')
         self.terms = 0     
         numSkills = 3   #  
      elif level == 'young':
         self.lastCareer = "Rogue"   
         self.age = Rpggen.roll('1d3+21')
         self.terms = 1
         numSkills = 5 # TODO right number?  Basic Training plus above.
      else:
         raise ValueError('level is an unknown value: %s' % level)

    # Three issues here: what skills, and what level (also equipment based on skills)
    # So we cycle through skills like this: 
    #   Brawling, Weapon, Something Else
    #   Until we are done with the skills the character has.
    # Most skills will be 0 or 1 at this point, but a few will be 2.
    # teens get 1 skill at 1, rest at 0    (20% change a 0 becomes a 2)
    # start get 3 skills at 1, rest at 0   (20% change a 1 to a 2)
    # young get 7 skills at 1, rest at 0   (20% change a 1 to a 2)

    # lucky means the character get more skills
      lucky = Rpggen.roll('1d3')-2
      numSkills += lucky
      if numSkills < 2:
          numSkills = 2
      if numSkills > 6:
          numSkills = 6          

      for idx in range(1, numSkills+1):
         if idx < 7:
            if (idx % 3) == 1:
               skill = Attribute(self.meleeSkills.use(),0)
               self.skills.append(skill)
            elif (idx % 3) == 2:
               skill = Attribute(self.weaponSkills.use(),0)
               self.skills.append(skill) 
            elif (idx % 3) == 0:
               skill = Attribute(self.otherSkills.use(),0)
               self.skills.append(skill)
            else:
               print('bad %d %d' % (idx, (idx % 3)))
         else:
             skill = Attribute(self.otherSkills.use(),0)
             self.skills.append(skill) 

      if level == 'teen':
         attr = Select.choose(self.skills,1)
         self.addToSkill(attr.name, attr.specific, 1)
      elif level == 'start':
         attrs = Select.choose(self.skills,2)
         for attr in attrs:
            self.addToSkill(attr.name, attr.specific, 1)  
      elif level == 'young':
         attrs = Select.choose(self.skills,2)
         for attr in attrs:
            self.addToSkill(attr.name, attr.specific, 1) 
      else:
         raise ValueError('level is an unknown value: %s' % level)                 	

      # Loop through each skills, and give any equipment that makes sense.
      for attr in self.skills:
         if attr.specific is not None:  
            self.equipmentTableOrDefault(attr.specific)

      # Figure out how much money he has 
      # TODO: refine algorithm
      # TODO: add bling
      pocket = int(Rpggen.roll('2d20')) * 10
      bank = int(Rpggen.roll('2d5')) * 100
      self.money = { 'pocket': pocket, 'bank': bank, 'pension': 0}

      # What is the thug carrying?
      if self.possessionsTable is not None:
         if self.money['bank'] > 300:
            num = Rpggen.roll('3d2')
         else:
            num = Rpggen.roll('2d2')
         self.possessions = Rpggen.find('PossessionsTable').rollRepeatedly(num)


      # Add some events

   def equipmentTableOrDefault(self, weapon, default=None):
      '''Note that this function assumes a table with name 'WeaponsX' for each skill with a
         specialization of X.  If oneis not found, then default is used, and if default is not
         set, then the specialization is used as a possetion.  (Which actually works better than
         you would expect.)
      '''
      if default is None:
         default = weapon
      tableName = 'Weapons'+weapon
      try: 
         equipment = Rpggen.finduse(tableName)
         if equipment is None or equipment == '':
            logging.warning('Using equipment table %s returned None or "".' % tableName)
         else:
            self.equipment.append(equipment)
      except:
         logging.warning('Table %s not found, but should have been in Settings.rpggen.' %
                        tableName)
         logging.warning(sys.exc_info()[1])    
         self.equipment.append(default+' Weapon')         

   def text(self):
      return self.strSmall()

   def html(self):
       doc, tag, text = Doc().tagtext()
       text('Name: %s --- %s --- %d years old' % (self.name, self.strUpp(),self.age))
       doc.asis('<br>')
       text('%s (%d term%s)              Cr%d' % (self.strCareer(), self.terms, ("s" if (self.terms!=1) else ""), self.availableMoney()))
       doc.asis('<p>')
       text(self.strSkills())
       if self.personality is not None:
          doc.stag('br') 
          text('Personality: %s' % ', '.join(self.personality))       
       doc.asis('<br>') 
       text('Equipment: %s' % ', '.join(self.equipment))
       doc.asis('<br>')
       text('Possessions: %s' % ', '.join(self.possessions))
       doc.asis('<br>')       
       text('Money: %d in pocket, %d in bank, %d in pension' %
                  (self.money['pocket'], self.money['bank'], self.money['pension']))
       doc.asis('<br>')
       #with tag('ol'):
       #   for history in self.history:
       #      with tag('li'):
       #         text(history)
       return doc.getvalue() 

   def htmlText(self):
      '''Returns a Young Thug in text format, but wrapped in the PRE tag, so it is actually
         HTML.
      '''
      return '<pre>'+self.strSmall()+'</pre>'  

   @classmethod
   def htmlPage(self, count=8):
      characters = []
      for ii in range(count):
         characters.append(YoungThug())
         characters[ii].generate()

      doc, tag, text = Doc().tagtext()
      with tag("html"):
         with tag("head"):
           pass
         with tag("body"):
            with tag("table", width = '100%', border=2, cellpadding=10, style='table-layout: fixed;'):
               for ii in range(int(count/2)):
                  with tag("tr", border=2):
                    for jj in range(2):
                      with tag('td', width = '50%', height = '25%', padding='15', border=2, style='word-wrap:break-word;'):
                        ch = characters[((ii*2)+(jj-1))-1]
                        tmp = ch.html()
                        doc.asis(tmp)
            doc.asis('<br>')
            with tag('small'):
               with tag('center'):
                  text('Traveller is a registered trademark of Far Future Enterprises.')
                  doc.stag('br')
                  text('Generated by Joshua Levy "Young Thugs" web server in 2017 version %s' % self.version)
      return doc.getvalue()

if __name__ == '__main__':    
    yt = YoungThug()
    yt.generate()
    print(yt.strSmall())
    print(Rpggen.toJson(yt))

    str = YoungThug.htmlPage()
    print(str)