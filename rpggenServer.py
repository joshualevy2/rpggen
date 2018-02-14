
# This python program takes an rpggen file, and serves it up as a micro
# service.  When you hit the root URL of the server, it will return the 
# table or template passed in as the second argument.
# So if you start it like this:
#    python ../rpggenServer.py malfunctions.rpggen MalfunctionDisplay
# then each time you hit this url:
#    http://localhost:1188/
# It will randomly generate a MalfunctionDisplay and return it.
#

from bottle import route, request, response, run, template, default_app
from Rpggen import Rpggen, Table
import sys

global outputFormat
global outputNumber
global table
global tableFormat


@route('/')
def basic():
   global table
   return table.use()
   #if outputFormat.contains('x'):
   #   pass
   #for _ in range(int(outputNumber)): 
   #   return Rpggen.finduse(sys.argv[2])

@route('/reload')
def reload():
   global table
   global tableFormat
   if tableFormat == 'json':
      Rpggen.load(sys.argv[1])
      table = Rpggen.find(sys.argv[2]) 
   else:
      table = Rpggen.loadLt(sys.argv[2])  
   return 'Reloaded the %s data file.' % sys.argv[1]

 
# execute only if run as a script    
if __name__ == "__main__":  
    global outputFormat
    global outputNumber
    global table
    global tableFormat
    outputFormat = 'text'
    outputNumber = '1'

    print(len(sys.argv))
    if len(sys.argv) != 2 and len(sys.argv)>3 :
        print('usage: python rpggenServer.py <filename> <table or template name>')
        print('    python rpggenServer.py Companies.lt  # File has one long table in it.')
        print('    python rpggenServer.py malfunctions.rppgen MalfunctionDisplay # File has json.')
        sys.exit(-1)
    
    # TODO: make this more object oriented with one method for both file types.
    if len(sys.argv) == 3:
        print("Running {0} with {1}".format(sys.argv[1],sys.argv[2]))
        tableFormat = 'json'
        Rpggen.load(sys.argv[1])
        table = Rpggen.find(sys.argv[2]) 
    else:
        print("Running table {0}".format(sys.argv[1]))
        tableFormat = 'lt'
        table = Rpggen.loadLt(sys.argv[1])
    run(host='0.0.0.0', port=1188, reloader=True, debug=True)
