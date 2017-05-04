
import sys
from rpggen import Rpggen, use 
   
# execute only if run as a script    
if __name__ == "__main__":  
    print("Testing {0} with {1}".format(sys.argv[0],sys.argv[1]))
    if len(sys.argv)!=2 :
        print('usage: python ' + sys.argv[0]+ ' <filename>')
        sys.exit(-1)
        
    Rpggen.load(sys.argv[1]) 

    all = Rpggen.dice.items()
    if len(all) == 0:
       print('There are no dice in this file.')
    else:
       print("For each dice, we print the name, the dice, and two rolls:")
       for id, dice in all:
          print("  "+id+" ("+dice['roll']+")")
          #print(dice)
          print("    "+Rpggen.use(dice))
          print("    "+use(id))
    
    print("Test all tables:")
    for id, table in Rpggen.tables.items() :
        print("  "+id+" ("+table['roll']+", "+str(len(table['rows']))+")")
        #print(table)
        print("    "+Rpggen.use(table))
        print("    "+use(id))

    all = Rpggen.templates.items()
    if len(all) == 0:
       print('There are no templates in this file.')
    else:        
       print("For each template, we print the name, and two results of use:")
       for id, template in all:
          print("  "+id)
          #print(template)
          print("    "+Rpggen.use(template))        
          print("    "+use(id))  
