import logging

from CepheusEngine import Career, CepheusEngine, Character
from rpggen import Rpggen, Table
from Traveller import Traveller

class CorporateRepo(Career):

   def __init__(self):
      super().__init__({'name': 'Corporate Repo',
      	    'qualifications': 'Int 5+',
             'survival': 'Int 4+',
             'commission': 'Soc 7+',
             'advancement': 'Int 6+',
             'reenlistment': '5+'})
      self.addData('Ranks',
      	          ['Crew/Agent', 'Lead', 'Manager','Sr.Manager','Director',
      	           'Sr.Director','Executive'])
      self.addData('Skills',
      	          ['Streetwise', None, 'GunCombat', None, None, None, None])      
      self.addTable('MaterialBenefits',
      	           ['+1 Str', '+1 Dex', '+1 End','MeleeCombat','+1 Edu','Athletics'])
      self.addTable('CashBenefits',
      	           ['+1 Str', '+1 Dex', '+1 End','MeleeCombat','+1 Edu','Athletics'])      	                 
      self.addTable('PersonalDevelopment',
      	           ['+1 Str', '+1 Dex', '+1 End','MeleeCombat','+1 Edu','Athletics'])
      self.addTable('ServiceDevelopment',
      	           ['Streetwise', 'Engineering', 'Bribery','Liaison','Recon','Mechanics'])
      self.addTable('SpecialistDevelopment',
      	           ['Zero-G', 'Comms', 'Admin','Electronics','Leadership','Jack-o-Trades'])
      self.addTable('AdvancedDevelopment',
      	           ['Computer', 'Gravitics', 'Piloting','Medicine?','Advocate','Tactics?'])
  
 #  def doBasicTraining(self, character):
 #     character.change(('skill','add','Liaison', '0'))

   def qualified(self,character):
   	qual = self.config['qualifications']
   	result = character.checkEnglish(qual)
   	character.log.append(('qualified', result))
   	return result

if __name__ == '__main__':    
   # Initialize the CepheusEngine environment, which also initializes the 
   # basic Traveller environment.
   logging.basicConfig(level=logging.INFO)
   cepheusEngine = CepheusEngine()
 
   # Initialize the CorporateRepo career
   crCareer = CorporateRepo()
 
   # Create an (empty) character to start with.
   crPerson = Character()
 
   # Do all the pre-career character generation steps.
   crPerson.createUpToCareer()
   crPerson.lastCareer = 'Corporate Repo'
 
   # Do basic training for this person
   crCareer.doBasicTraining(crPerson)

   endReason = None 
   while endReason is None:
      endReason = crCareer.doOneTerm(crPerson)

   crPerson.endReason = endReason

   print(crPerson.strSmall())
   print(crPerson.strHistory())
   #cr.printTest()