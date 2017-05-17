development = True
from bottle import route, request, response, run, template, default_app
import sys

from YoungThugs import YoungThug

if development:
   sys.path.append('..')
else:
   sys.path.append('/home/joshualevy/rpggen')

from rpggen import Rpggen, Table

@route('/request')
def r():
    return str(request.query.format =='')

@route('/yt/help')
def ytHelp():
    return 'This server returns one young thug in plain text format'

@route('/yt')
def youngthug():
   yt = YoungThug()
   yt.generate()
   if request.query.format == '' or request.query.format == 'html':
      return yt.html()
   elif request.query.format == 'htmlText':
    return yt.htmlText()      
   elif request.query.format == 'text':
   	return yt.strSmall()
   elif request.query.format == 'htmlPage':
      return yt.htmlPage()   	  
   else:
   	return ('Unknown format query variable.'
   	  	     '  Right now, only "text", "html", and "htmlPage" is supported.')

if development:
   # bottle.debug(True)
   run(host='localhost', port=1188, reloader=True, debug=True)
else:
   # bottle.run(server='paste')
   application = default_app()