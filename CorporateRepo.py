import logging

from CepheusEngine import Career, CepheusEngine, Character
from Rpggen import Rpggen, Table
from Traveller import Traveller

class CorporateRepo(Career):
   '''This class repsents one career.
   '''

   def __init__(self):
      super().__init__({'name': 'Corporate Repo',
      	    'qualifications': 'Int 5+',
             'survival': 'Int 4+',
             'commission': 'Soc 7+',
             'advancement': 'Int 6+',
             'reenlistment': '5+'})
      self.addData('Ranks',
      	          ['Crew', 'Specialist', 'Agent', 'Lead', 'Manager','Director',
      	           'Executive'])
      self.addData('Skills',
      	          ['Streetwise', None, 'GunCombat', None, None, None, None])     
      self.addTable(Table('MaterialBenefits',
      	                  ['Weapon', 'Explorer\' Society', 'Weapon', 'Mid Passage',
                           'High Passage', 'High Passage or Starship']))
      self.addTable(Table('CashBenefits',
      	                  ['cr2000', 'cr10000', 'cr10000', 'cr10000', 'cr20000', 'cr40000',
                           'cr100000']))      	                 
      self.addTable(Table('PersonalDevelopment',
      	                  ['+1 Str', '+1 Dex', '+1 End','MeleeCombat',
                           'Vehicle','Athletics']))
      self.addTable(Table('ServiceDevelopment',
      	                  ['Streetwise', 'Engineering', 'Bribery', 'Liaison',
                           'Recon', 'Mechanics']))
      self.addTable(Table('SpecialistDevelopment',
      	                  ['Zero-G', 'Comms', 'Admin', 'Tactics', 'Leadership',
                           'Jack-o-Trades']))
      self.addTable(Table('AdvancedDevelopment',
      	                  ['Computer', 'Gravitics', 'Piloting', 'Navigation',
                           'Advocate', 'Electronics']))

   def qualified(self,character):
   	qual = self.config['qualifications']
   	result = character.checkEnglish(qual)
   	character.log.append(('qualified', result))
   	return result

if __name__ == '__main__':    
   # Initialize the CepheusEngine environment, which also initializes the 
   # basic Traveller environment.
   #logging.basicConfig(level=logging.INFO)
   cepheusEngine = CepheusEngine()
 
   # Initialize the CorporateRepo career
   crCareer = CorporateRepo()
 
   # Create an (empty) character to start with.
   crPerson = Character()

   crPerson.createUsingTimeline(career=crCareer)

   print(crPerson.strSmall())
   print(crPerson.strHistory())
   #cr.printTest()