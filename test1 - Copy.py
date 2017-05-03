
import json, re, random, sys
from bottle import SimpleTemplate

def use(arg) :
    return rpggen.finduse(arg)

class rpggen:
    raw = {}
    tables = {}
    templates = {}
    keywords = {}
    rolls = {}
    
    def type(obj) :
        if "text" in d :
            return 'template'
        else :
            return 'table'
            
    def use(obj) :
        if obj['_type'] == 'template' :
           template = SimpleTemplate(obj['text'])
           return template.render(use=use,rpggen=rpggen)
        elif obj['_type'] == 'table' :
           return obj['roll']           
        else :
           return 'Error: wrong object type'
           
    def finduse(name):
        for d in rpggen.raw :
            if d['id'] == name :
               return rpggen.use(d)
                
    def load(filename) :
      rpggen.raw = json.load(open(sys.argv[1], 'r'))
      for d in rpggen.raw :
        #print(d)
        #print(d['id'])
        if "text" in d :
            print("loaded template: "+d['id'])
            d['_type'] = 'template'
            rpggen.templates[d['id']] = d
        else :
            startnum = re.compile(r"^[0123456789]+")
            maxnum = -sys.maxsize
            minnum = sys.maxsize
            print("loaded table: "+d['id'])
            d['_type'] = 'table'
            for k in d :
               #print(startnum.search(k))
               if startnum.search(k) :
                   num = int(k)
                   if num > maxnum :
                       maxnum = num
                   if num < minnum :
                       minnum = num
            if not 'roll' in d :           
                d['roll'] = str(minnum)+"d"+str(int(maxnum/minnum))
                
            rpggen.tables[d['id']] = d    
   
# execute only if run as a script    
if __name__ == "__main__":     
    if len(sys.argv)<3 or len(sys.argv)>4:
        print('usage: python ' + sys.argv[0]+ ' <filename> table-or-template [count]')
        sys.exit(-1)
    rpggen.load(sys.argv[1])
    """
    rpggen.raw = json.load(open(sys.argv[1], 'r'))
    for d in rpggen.raw :
        #print(d)
        #print(d['id'])
        if "text" in d :
            print("loaded template: "+d['id'])
            d['_type'] = 'template'
            rpggen.templates[d['id']] = d
        else :
            startnum = re.compile(r"^[0123456789]+")
            maxnum = -sys.maxsize
            minnum = sys.maxsize
            print("loaded table: "+d['id'])
            d['_type'] = 'table'
            for k in d :
               #print(startnum.search(k))
               if startnum.search(k) :
                   num = int(k)
                   if num > maxnum :
                       maxnum = num
                   if num < minnum :
                       minnum = num
            if not 'roll' in d :           
                d['roll'] = str(minnum)+"d"+str(int(maxnum/minnum))
                
            rpggen.tables[d['id']] = d
    """     
    print(rpggen.finduse(sys.argv[2]))

