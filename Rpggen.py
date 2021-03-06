
import os

import  json, logging, re, random, sys, string

from bottle import SimpleTemplate
from jsoncomment import JsonComment

def use(arg):
    return Rpggen.finduse(arg)
    
class Dice:
   dice = ''
 
   def __init__(self,name,dice=None):
      # If is the first argument which is optional
      if dice is None:
         dice = name
         name = None
      self.dice = dice
      if name is not None:   
         #DEBUGGING print('adding table %s' % name)
         #TODO Rpggen.tables[name] = self
         pass
         
   def roll(self):
      return self.use()
      
   def use(self):
      return Rpggen.roll(self.dice)

class Rpggen:
    '''This is a singleton class (so it operates more like a library.
    '''        
    tables = {}
    templates = {}
    keywords = {}
    dice = {}
    testData = None
    customizations = {}
    raw = []

    @classmethod
    def clear(cls):
       for (name, tab) in cls.tables.items():
          tab.clear()

    @classmethod
    def getCustomization(cls, name, default=None):
      '''Returns the customization value, or the second argument, if that
         customization is not set, or None if the second argument is empty.
      '''
      if cls.customizations is None:
         return default
      try:
         result = cls.customizations[name]
         return result
      except KeyError:
         return default    

    def getNth(table,nth):
       for k,v in table['rows'].items():
          ii += 1
          if ii == nth:
             return (k,v)
       raise ValueError('Not that many (%d) items in the table.' % nth)
    
    def getOneResult(table):
       rows = table['rows']
       length = len(rows)
       nn = Rpggen
       (k,v) = getNth(table,nn)
       return v
    
    def getOneEntry(table):
       rows = table['rows']
       length = len(rows)
       nn = Rpggen
       (k,v) = getNth(table,nn)
       return (k,v)  

    @classmethod
    def setAllCustomizations(cls, customizations):
      '''Sets all customizations by replacing whatever is there with those listed
         in the argument.  Previous customizations are lost, even if their is non-standard
         similar customization in the argument.
      '''
      cls.customizations = customizations

    @classmethod
    def setCustomization(cls, name, value):
      '''Sets one customization.  Either changes the value, if it already exists,
         or creates it new, with the given value.
      '''
      cls.customizations[name] = value
    
    @classmethod
    def setup(cls, customizations=None, logger=None):
       if cls.customizations is not None:
          cls. setAllCustomizations(customizations)
       if logger is not None:
          pass

    @classmethod
    def use(cls, obj) :
        #print(obj)
        if isinstance(obj,"".__class__) :
            #print("roll: "+obj)
            return str(cls.roll(obj))
        elif obj['_type'] == 'dice' :
            #print("dice: "+obj['roll'])
            return str(cls.roll(obj['roll']))
        elif obj['_type'] == 'template' or 'text' in obj :
           template = SimpleTemplate(obj['text'])
           return template.render(use=use,rpggen=Rpggen)
        elif obj['_type'] == 'table' or ('roll' in obj and 'rows' in obj) :
           roll = cls.roll(obj['roll'])
           for row in obj['rows'] :
              if roll >= row.start and roll <= row.stop :
                  if row.result != "" :
                      template = SimpleTemplate(row.result)
                      finalResult = template.render(use=use,rpggen=Rpggen)
                      #print("From {0} raw result {1}, final result {2}".format(obj['id'],row.result,finalResult))
                      return finalResult
                  else :
                      return ""
           return "Typo in table! Rolled a "+roll+" but no row for that: "+str(obj['rows'])
        else :
           return 'ERROR: wrong object type'

    @classmethod
    def find(cls, name, debug=False):
       #print("finduse: "+name)   
       if type(name) is list:
          longname = ''.join(name)
          tab = cls.tables[name]
          if tab is None:
             if len(name) == 1:
                return cls.find(name,debug)
             else:
                return cls.find(name[:-1],debug)   
             return find 
          pass
       else:
          # It's a string, the normal case
          try:
           tab = cls.tables[name]
           return tab 
          except:   
           if debug:
              print(Table.names())
              print("ERROR: Could not find a table or template named "+name+" and it doesn't look like a dice roll.\n")
           return None

    @classmethod
    def finduse(cls, name, debug=False):
        if debug:
           print('Calling Rpggen.finduse(%s)' % name)  
        try:
           tab = cls.find(name,debug)
           if tab is None:
              raise KeyError
           return tab.use(debug=debug)  
        except KeyError:
           if debug:
              print('No Rpggen.tables[%s]' % name)
              print(sys.exc_info()[1])
           pass
        # TODO: why look in both raw and tables?
        for d in cls.raw :
            if d['id'] == name :
               if debug:
                  print('Found in Rpggen.raw')              
               return cls.use(d)   
        try:
           re.split(r'[d+-]',name)  # JCL used to have backslashes before + and -
           return str(cls.roll(name))
        except ValueError:
           pass   
        print(Table.names())
        print("ERROR: Could not find a table or template named "+name+" and it doesn't look like a dice roll.\n")
        raise ValueError("ERROR: Could not find a table or template named "+name+" and it doesn't look like a dice roll.")

    @classmethod     
    def load(cls, filename, optional=False, debug=False):
      '''Loads an rpggen file into the program.
         optional=True if the file is optional: no error message if not found.
      '''
      startnum = re.compile(r"^[0123456789]+")
      diceRE = re.compile(r"^[0123456789]*d[0123456789]+")
      if not os.path.isfile(filename) and optional:
         return
      with open(filename, 'r') as file:
         jsonComment = JsonComment(json)
         cls.raw = jsonComment.load(file)
      for d in cls.raw :
        if "text" in d :
            #print("loaded template: "+d['id'])
            d['_type'] = 'template'
            if re.search(r'.tmpl$',d['text']) :
                with open(d['text'],'r') as template_file :
                    d['text'] = template_file.read()
            cls.templates[d['id']] = d
        if len(d) == 1 :
            for k in d :    # there is only one
                id = k
            d['id'] = id
            if isinstance(d[k], str) :
                if diceRE.search(d[k]) :
                    d['_type'] = 'dice'
                    d['roll'] = d[id]
                cls.dice[d['id']] = d
            else :
                d['_type'] = 'table'
                d['rows'] = [ ]
                ii = 1
                for item in d[k] :
                    row = Row()
                    row.result = item
                    row.start = row.stop = ii
                    ii += 1
                    d['rows'].append(row)
                d['roll'] = "1d"+str(ii)
                cls.tables[d['id']] = d
            #print("singleton"+str(d))
        else :
            tableId = d['id']
            if debug == True:
               print("loading table: "+tableId)
            rows = {}
            maxnum = -sys.maxsize
            minnum = sys.maxsize
            for k in d :
                if startnum.search(k):
                    rows[k] = d[k]
            tab = Table(tableId, rows)
            if not 'unique' in d:
               tab.setUnique(False)
            else:
               tab.setUnique(d['unique'])

    @classmethod
    def loadLt(cls, filename):
       '''Loads an rpggen file into the program.
          Throws an exception if the file is not found.
       '''
       tableName = None
       entries = []
       removeFirstToken = False
       with open(filename) as file:
          content = file.readlines()
       for line in content:
          line = line.strip()
          if len(line) == 0:
             # Blank lines are ignored
             pass
          elif not line[0] == '#':
             # Most lines become entries in the table.
             if removeFirstToken:
                # Cuts off the first token (whitespace seperated) from line. Keeps the rest.
                entries.append(line.split(None, 1)[1])
             else:
                entries.append(line)
          else:
             # Lines that start with a # are comments, so mostly ignored, but some
             # are special controls.            
             if 'RemoveFirstToken' in line:
                removeFirstToken = True
             if 'Name' in line:
                tableName = line.split(None, 2)[2]
       tab = Table(tableName, entries)
       return tab

    @classmethod
    def roll(cls, diceStr, debug=False):
       '''Rolls RPG style dice.
          Pass debug=True to print out debugging information.
       '''
       # TODO: Test and document
       d66match = re.search(r'[dD]6(6+)',diceStr)
       if d66match is not None and cls.getCustomization('d66support', False):
          return cls.rollconcat(diceStr)   
       match = re.search(r'([0-9]+o)?([0-9]+)?([dDsS])([0-9]+)([-+][0-9]+)?',diceStr)
       if match == None:
          raise ValueError('%s was not a dice roll' % diceStr)
       if debug:
          print('%s -> %s-%s-%s-%s' % 
                     (diceStr, match.group(1),match.group(2),match.group(3),match.group(4)))
       if match.group(1) is not None:
          raise ValueError('No support for "o" dice type.')
       total = 0
       diceNum = match.group(2)
       if diceNum is None :
           diceNum = 1
       else:
           diceNum = int(diceNum)
       try:
          diceSize = int(match.group(4))
       except:
          raise ValueError('Error in dice size while rolling %s.' % diceStr)
       for ii in range(diceNum) :
           if cls.testData == None:
              total += random.randint(1,diceSize)
           else:
              # TODO if testData out of range
              total += cls.testData
       diceAdjustment = match.group(5)
       if diceAdjustment is not None :
           try:
              adjustment = int(diceAdjustment)
              total += adjustment
           except:
              raise ValueError('Error in adjustment while rolling %s in the %s part.' % (diceStr, diceAdjustment))
       if debug:
          print('Rpggen.roll returns %d' % total)       
       return total

    @classmethod
    def rollconcat(cls, diceStr):
       '''Supports d6 only.
          Traveller
       '''
       total = 0
       numDice = len(diceStr)-1
       for ii in range(numDice) :
           total = total * 10
           if cls.testData == None:
              total += random.randint(1,6)
           else:
              # TODO if testData out of range
              total += cls.testData
       return total

    @classmethod
    def toJson(cls, obj):
       '''Takes a Python object, such as a Character, and returns it as a json string.
          This is a generic version, but if you create a new type of object that needs
          a more specific version, you should write a method in that class.
       '''
       return json.dumps(obj, default=lambda o: o.__dict__, 
                     sort_keys=True, indent=4)

    def setUnique(setting):
       self.unique = setting
       self.clear()
       
    @classmethod       
    def chars(cls, num, fro=string.ascii_lowercase) :
        #TODO non-random rolling
        result = ""
        for ii in range(num) :
            result += (random.choice(fro))
        return result      

class Select:

   @classmethod
   def choose(cls,myList, number=1, debug=False):
      if debug:
         print('Select.choose(%s,%d)' % (myList,number))
      if number == 1:
         if Rpggen.testData == None:
            return random.choice(myList)
         else:
            if Rpggen.testData < len(myList):
               return myList[Rpggen.testData-1]
            else:
               # TODO if testData out of range
               pass
      else:
         result = []
         for idx in range(number):
            result.append(random.choice(myList))
         return result

class Table:
   id = None
   dice = None
   rows = []
   unique = False
   
   def __init__(self, name, values=None, unique=None, debug=False):
      # If is the first argument which is optional
      if debug:
         print('new Table with: name=%s, values=%s, unique=%s' %
               name, values, unique)
      if values is None:
         values = name
         name = None
      self.id = name
      self.dice = None
      self.rows = []
      if not unique is None:
         self.setUnique(unique)
      lineNum = 1
      if type(values) is list:
         self.dice = '1d%d' % len(values)
         for value in values :
            row = Row()
            row.start = row.stop = lineNum
            lineNum += 1
            row.result = value
            self.rows.append(row)
      elif type(values) is dict:
         maxnum = -sys.maxsize
         minnum = sys.maxsize
         for key, value in values.items() :
            if key == 'roll':
               self.dice = value
            else:
               row = Row()
               sss = key.split('-')
               row.start = int(sss[0])
               row.stop = row.start
               if len(sss) == 2 :
                  row.stop = int(sss[1])               
               row.result = value
               self.rows.append(row) 
               # keeping track of smallest and largest if needed to create the roll
               if row.stop > maxnum :
                  maxnum = row.stop
               if row.start < minnum :
                  minnum = row.start
         if self.dice is None :
            self.dice = str(minnum)+"d"+str(int(maxnum/minnum))                            
      else:
         raise TypeError('The values argument of this function must be a list or a dict, but is a %s' % type(x))      
      if name is not None:
         if debug:
            print('Creating Table with adding %s to Rpggen.tables' % name)
         Rpggen.tables[name] = self
   
   def internal_check(self):
      printName = self.id
      if self.id is None:
         printName = "Not Set"
      if self.dice is None:
         raise ValueError('Table %s has no dice set.' % printName)
      if len(self.rows) == 0:
         raise ValueError('Table %s has no rows in it.' % printName)
      for row in self.rows:
         if row.result is None:
            logging.warning('Table %s has None as results.' % printName)

   def clear(self):
      for row in self.rows:
        row.used = False

   @classmethod
   def names(cls):
       return ", ".join(Rpggen.tables.keys())

   def results(self):
      results = []
      for row in self.rows:
         results.append(row.result)
      return results
      
   def roll(self):
      return self.use()
 
   def rollRepeatedly(self, num, unique=True):
      return self.useRepeatedly(num, unique)

   def smallStr(self):
      results = []
      for row in self.rows:
         results.append(row.smallStr())
      return results

   def setUnique(self, value):
      self.unique = value
      if value:
         self.clear()

   def use(self, partof=None, debug=False):
      self.internal_check()
      if debug:
         print('Calling Table.use %s %s %d unique=%s' % (self.id, self.dice, len(self.rows), self.unique))
      roll = Rpggen.roll(self.dice, debug=debug)
      for row in self.rows:
         if debug:
            print('%d %d-%d %s' % (roll, row.start, row.stop, (row.start <= roll <= row.stop)))
         if row.start <= roll <= row.stop:
            # If this row has been used, and the table is rolling uniquely (in general)
            # Then we cycle through the table to find any unused entry.
            if self.unique and row.used:
               # Can not use what we rolled, so see if there is something else we can use.
               row = None
               for row2 in self.rows:
                 if not row2.used:
                    row = row2
                    break
               if row is None:   
                  if partof is None:
                     partof = 1 
                  raise ValueError('Rolling uniquely on %s (%d times), but no rows are unused. '
                                   'That table has %d rows.' % 
                                   (self.id, partof, len(self.rows)))
            # We've now found the right row, so mark it as used, and return it (or it's template)
            row.used = True
            if row.result != '' :
               if debug:
                  print('Raw result is %s %s' % (row.smallStr(), row.result))
               template = SimpleTemplate(row.result)
               finalResult = template.render(use=use,rpggen=Rpggen)
               if debug:
                  print('Returning %s' % str(finalResult))
               return finalResult
            else :
               return ''
      print('Should never get here 666')         

   def useRepeatedly(self, num, unique=True):
      results = []
      wasunique = self.unique
      if unique:
         self.setUnique(True)
      for nn in range(num):
         results.append(self.use(partof=num))
      self.setUnique(wasunique)
      return results


class Template:
   def __init__(self,name,template=None):
      # If is the first argument which is optional
      if template is None:
         template = name
         name = None
      self.id = name
      self.template = SimpleTemplate(template)

   def internal_check(self):
      printName = self.id
      if self.id is None:
         printName = "Not Set"
      if self.template is None:
         raise ValueError('Template %s has no template set.' % printName)    

   def use(self):
      return self.template.render(use=use,rpggen=Rpggen)

class Row:
   start = -1
   stop = -1
   result = ""
   used = False
    
   def smallStr(self):
      if self.start == self.stop:
         return '[%d: %s]' % (self.start, self.result)
      return '[%d-%d: %s]' % (self.start, self.stop, self.result)

# execute only if run as a script
if __name__ == "__main__":
    #print(len(sys.argv[1]))
    if len(sys.argv) == 1:
        # No arguments test something  then print out usage message
        print('d6 = %d' % Rpggen.roll('d6'))
        Rpggen.testData = None
        print('3d6 = %d' % Rpggen.roll('3d6'))
    if len(sys.argv)<3 or len(sys.argv)>4 :
        print('usage: python ' + sys.argv[0]+ ' <filename> <tablename> [<count>]')
        sys.exit(-1)

    Rpggen.load(sys.argv[1])

    if len(sys.argv)==3 :
        print(Rpggen.finduse(sys.argv[2]))
    else :
        for ii in range(int(sys.argv[3])) :
            print(Rpggen.finduse(sys.argv[2]))
