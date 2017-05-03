
import sys

from rpggen import Rpggen        
   
# execute only if run as a script    
if __name__ == "__main__":
    count = 20
    #print(len(sys.argv[1]))
    if len(sys.argv)<3 or len(sys.argv)>4 :
        print('usage: python ' + sys.argv[0]+ ' <filename>')
        sys.exit(-1)
    
    if len(sys.argv)==4 :
        count = int(sys.argv[3])
        
    Rpggen.load(sys.argv[1]) 
    
    print("""<html>
    <head>
    </head>
    <body>
    <table>
    <tr><th align=right>Roll</th><th>Result</th></tr>
    """)
    for ii in range(count) :
        print("<tr><td align='right'>"+str(ii+1)+"</td><td>"+Rpggen.finduse(sys.argv[2])+"</td></tr>")
    print("""</table>
    </body>
    </html>
    """)
