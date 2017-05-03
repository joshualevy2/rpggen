
import sys
from rpggen import * 
   
# execute only if run as a script    
if __name__ == "__main__":     
    if len(sys.argv)!=3 :
        print('usage: python ' + sys.argv[0]+ ' <filename>')
        sys.exit(-1)
        
    rpggen.load(sys.argv[1]) 
       
    print("Test all tables:")
    for obj in rpggen.raw :
        print("    "+obj['id']+" ("+obj['_type']+")")
        if sys.argv[2]  == obj['id'] :
            rndobj = obj
    if rndobj['_type'] != 'template' :
        print("Random: "+rndobj['roll'])
    
    print("Use object twice:")
    print(rpggen.finduse(sys.argv[2]))
    print(rpggen.use(rndobj))
    
    print("raw data structure:")
    print(rndobj)