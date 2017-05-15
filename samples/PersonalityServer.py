development = True
from bottle import route, request, response, run, template, default_app
import json
import sys
from yattag import Doc

from YoungThugs import YoungThug

if development:
   sys.path.append('..')
else:
   sys.path.append('/home/joshualevy/rpggen')

from rpggen import Rpggen, Table


# Formatting functions
class formatting():
 def html(results):
   #return "<pre>"+str(results)+"</pre>"
   doc, tag, text = Doc().tagtext()
   with tag("html"):
      with tag("head"):
         pass
      with tag("body"):
         for result in results:
            doc.asis('<br>')
            text(result)
   return doc.getvalue()

 def text(results):
   return ', '.join(results)   

# Routing functions

@route('/p/info')
def info():
   doc, tag, text = Doc().tagtext()
   with tag("html"):
      with tag("head"):
         pass
      with tag("body"):
         with tag('p'):
            text('This server returns personalities for NPCs and PCs in role playing games.'+
                 'Examples of use include:')
         with tag('ul'):
            with tag('li'):
               text('https://joshualevy.pythonanywhere.com/p/info To see this help message.')  
            with tag('li'):
               text('https://joshualevy.pythonanywhere.com/p/1000words/3 ')  
            with tag('li'):
               text('https://joshualevy.pythonanywhere.com/p/100words/30 ')                
         with tag('p'):
            with tag('b'):
               text('1000words')
            text(': Choose personality traits from a list of 1000 words.')
         with tag('p'):
            with tag('b'):
               text('100words')
            text(': Choose personality traits from a list of 100 words.')    
         with tag('p'):
               text('The following format varibles are supprted:')
               doc.asis('html: Results formatted in html; best for human viewing.<br>')
               doc.asis('text: Plain text.  Looks ugly in browsers.<br>')
               doc.asis('htmlText: The same as text, but formatted so that it looks ok in html.<br>')
               doc.asis('json: your results, encoded as a list, ready for use by other programs.  '+
                        'You can think of this as the REST API for a personality service.<br>')
         with tag('p'):
            with tag('b'):
               text('My Reuqest To Users')
         with tag('p'):
            text('Please send me feedback on the personality traits this web page gives you! '+
                 'You can send email to joshualevy2 @ hotmail dot com, or join the discussion '+
                 'on the CoTI software forum here: **')   
         with tag('p'):
            with tag('b'):
               text('Advice On Using This Website')
         with tag('p'):
            text('For NPCs, I think that the best way to generate a personality is to run this command:') 
         with tag('tt'):
            text('https://joshualevy.pythonanywhere.com/p/1000words/3') 
         with tag('p'): 
            text("And then toss out any traits that don't fit, and arrage the rest in order of "+
                 "importance.  Most important first.  It's quick, easy, and I've found that it "+
                 "gives results which are both good and useful. If you find that you are tossing "+
                 "out more than 2 traits on average, then start out with 4 or more.  The goal is "+
                 "to end up with 2 or 3 good ones, in the order you like.")  
         with tag('p'):
            text('For PCs, the method above works well, however **:') 
         with tag('tt'):
            text('https://joshualevy.pythonanywhere.com/p/1000words/3') 
         with tag('p'): 
            text("And then toss out any traits that don't fit, and arrage the rest in order of "+
                 "importance, most important first.  It's quick, easy, and I've found that it "+
                 "gives results which are both good and useful. If you find that you are tossing "+
                 "out more than 2 traits on average, then start out with 4 or more.  The goal is "+
                 "to end up with 2 or 3 good ones, in the order you like.") 
   return doc.getvalue()   

@route('/p/<method>')
@route('/p/<method>/<num:int>')
def PersonalityTraits1000(method, num=3):
   results = []
   if method == "1000words":   
      results = PersonalityTraits1000Tab.useRepeatedly(num, unique=True)
   elif method == "100words":
      results = PersonalityTraits100Tab.useRepeatedly(num, unique=True)
   else:
      return 'Method is not supported.  Supported methods are: 1000words and 100words.'
   if request.query.format == '' or request.query.format == 'html':
      return formatting.html(results)
   elif request.query.format == 'htmlText':
      return '<pre>'+formatting.text(results)+'</pre>'
   elif request.query.format == 'json':
      return json.dumps(results, default=lambda o: o.__dict__, 
                     sort_keys=True, indent=4) 
   elif request.query.format == 'text':
      return formatting.text(results) 	  
   else:
   	  return ('Unknown format query variable.'
   	  	      '  Right now, only "text", "html", "htmlText, and "htmlPage" is supported.')

PersonalityTraits100Tab = Rpggen.loadLt("PersonalityTraits100.lt")
PersonalityTraits1000Tab = Rpggen.loadLt("PersonalityTraits.lt")
if development:
   # bottle.debug(True)
   run(host='localhost', port=1188, reloader=True, debug=False)
else:
   # bottle.run(server='paste')
   application = default_app()