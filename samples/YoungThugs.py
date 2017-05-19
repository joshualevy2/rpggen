import random
import sys
import unittest
import json
from yattag import Doc

sys.path.append('..')
from CepheusEngine import Character
from GetFromWeb import GetFromWeb
from Rpggen import Rpggen, Select, Table
from Traveller import Attribute, Traveller

# TODO Why not CepheusEngine.Character?
class YoungThug(Character):

   version = '0.1'

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
   possessionsTable = Table('PossetionsTable',
                            ['Key', 'Legal Drugs', 'Illegal Drugs', 'Gambling Materials',
                             'Gear Bag', 'Shades', 'Pet', 'Religious Figurine', 'Feather',
                             'Rock'])

   def __init__(self):
      super().__init__()
      Rpggen.clear()
      try:
         Rpggen.load("YoungThugs.rpggen")
      except:
         print('Warning: could not find data file YoungThugs.rpggen.') 
         print(sys.exc_info()[1])       

   def generate(self):
      Rpggen.clear()
      self.name = GetFromWeb.get('names')
      self.lastCareer = "No Career"    
      self.str = Rpggen.roll('2d5+2')
      self.dex = Rpggen.roll('2d5+2')
      self.end = Rpggen.roll('2d5+2')
      self.int = Rpggen.roll('2d5')
      self.edu = Rpggen.roll('2d2')
      self.soc = Rpggen.roll('2d3')

      try:
         personalityTable = Rpggen.loadLt("PersonalityTraits.lt")
      except:
         personalityTable = None
      if personalityTable is not None:
         self.personality = personalityTable.rollRepeatedly(3, unique=True)

      level = Select.choose(['teen','start', 'young'])
      if level == 'teen':
         self.age = Rpggen.roll('1d3+15')
         self.terms = 0  
         numSkills = 3   # TODO right number?     
      elif level == 'start':
         self.age = Rpggen.roll('1d3+17')
         self.terms = 0     
         numSkills = 5   #  
      elif level == 'young':
         self.lastCareer = "Rogue"   
         self.age = Rpggen.roll('1d3+21')
         self.terms = 1
         numSkills = 9 # TODO right number?  Basic Training plus above.
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
      lucky = (Rpggen.roll('1d5') == 1)
      for idx in range(1, numSkills):
         if idx < 7:
          if idx % 3 == 1:
             skill = Attribute(self.meleeSkills.use(),0)
             self.skills.append(skill)
          if idx % 3 == 2:
             skill = Attribute(self.weaponSkills.use(),0)
             self.skills.append(skill) 
          if idx % 3 == 0:
             skill = Attribute(self.otherSkills.use(),0)
             self.skills.append(skill)
         else:
             skill = Attribute(self.otherSkills.use(),0)
             self.skills.append(skill)       	

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
            num = Rpggen.roll('3d3')
         else:
            num = Rpggen.roll('2d2')
         self.possessions = Rpggen.find('PossetionsTable').rollRepeatedly(num)



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
         self.equipment.append(Rpggen.finduse(tableName))
      except:            
         self.equipment.append(default)

   def text(self):
      return self.strSmall()

   def html(self):
       doc, tag, text = Doc().tagtext()
       text('Name: %s        %s  %d years old' % (self.name, self.strUpp(),self.age))
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
       #text('Possessions: %s' % ', '.join(self.possesions))
       doc.asis('<br>')       
       text('Money: %d in pocket, %d in bank, %d in pension' %
                  (self.money['pocket'], self.money['bank'], self.money['pension']))
       doc.asis('<br>')
       return doc.getvalue() 

   def htmlText(self):
      '''Returns a Young Thug in text format, but wrapped in the PRE tag, so it is actually
         HTML.
      '''
      return '<pre>'+self.strSmall()+'</pre>'  

   @classmethod
   def htmlPage(self, count=10):
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
                        ch = characters[ii+(jj-1)]
                        tmp = ch.html()
                        doc.asis(tmp)
            doc.asis('<br>')
            with tag('small'):
               with tag('center'):
                  text('Generated by Joshua Levy "Young Thugs" web server in 2017 version %s' % self.version)
      return doc.getvalue()

if __name__ == '__main__':    
    yt = YoungThug()
    yt.generate()
    print(yt.strSmall())
    print(Rpggen.toJson(yt))
    #print(json.dumps(yt, default=lambda o: o.__dict__, 
    #                 sort_keys=True, indent=4))

    str = YoungThug.htmlPage()
    print(str)