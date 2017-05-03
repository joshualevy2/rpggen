
import sys
from rpggen import * 
   
# execute only if run as a script    
if __name__ == "__main__":  
    print("Testing {0} with {1}".format(sys.argv[0],sys.argv[1]))
    if len(sys.argv)!=2 :
        print('usage: python ' + sys.argv[0]+ ' <filename>')
        sys.exit(-1)
        
    rpggen.load(sys.argv[1]) 

    print("Test all dice:")
    for id,dice in rpggen.dice.items() :
        print("  "+id+" ("+dice['roll']+")")
        #print(dice)
        print("    "+rpggen.use(dice))
        print("    "+use(id))
        
    print("Test all tables:")
    for id,table in rpggen.tables.items() :
        print("  "+id+" ("+table['roll']+", "+str(len(table['rows']))+")")
        #print(table)
        print("    "+rpggen.use(table))
        print("    "+use(id))
        
    print("Test all templates:")
    for id,template in rpggen.templates.items() :
        print("  "+id)
        #print(template)
        print("    "+rpggen.use(template))        
        print("    "+ruse(id))  

