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

if development:
   baseUrl = 'http://localhost:1188'
else:
   baseUrl = 'http://joshualevy.pythonanywhere.com'

globalHelp = ''

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

 def link(tag, text, url):
     with tag('a', href=url):
        text(url)   

# Routing functions

@route('/help')
def help():
   doc, tag, text = Doc().tagtext()
   with tag("html"):
      with tag("head"):
         pass
      with tag("body"):
         with tag('p'):
           text('This is an experimental server run by Joshua Levy.')
         with tag('p'):
           text('You can always goto %s/help to get this help message.' % baseUrl)  
         with tag('p'):
            text('This server can provide serveral micro-services, which are described '+
                 'below:') 
         doc.asis(globalHelp)              
   return doc.getvalue()


def pGlobalHelp():
   global globalHelp
   doc, tag, text = Doc().tagtext()
   with tag('h2'):
         text('Personality Servers: Personalities for NPCs and PCs')
   with tag('blockquote'):
         text('Get help: ')
         formatting.link(tag, text, '%s/p/help' % baseUrl)
         doc.stag('br')
         text('Try it: ')
         formatting.link(tag, text, '%s/p/1000words/3?format=json' % baseUrl)
         doc.stag('br')
         text('Or try this: ')
         formatting.link(tag, text, '%s/p/1000words/3?format=html' % baseUrl)

   globalHelp += doc.getvalue()   

pGlobalHelp()   

@route('/p/help')
def pHelp():
   doc, tag, text = Doc().tagtext()
   with tag("html"):
      with tag("head"):
         with tag('style'):
            text('''dl {
   # border: 3px double #ccc;
   # padding: 0.5em;
  }
  dt {
    float: left;
    clear: left;
    width: 100px;
    text-align: right;
    font-weight: bold;
  }
  dt::after {
    content: ":";
  }
  dd {
    margin: 0 0 0 110px;
    padding: 0 0 0.5em 0;
  }''')
      with tag("body"):
         with tag('p'):
            text('This server returns personalities for NPCs and PCs in role playing games.  '+
                 'Examples of use include:')
         with tag('ul'):
            with tag('li'):
               with tag('a', href='https://joshualevy.pythonanywhere.com/p/info'):
                 text('%s/p/help' % baseUrl)
               text(' To see this help message.')  
            with tag('li'):
               formatting.link(tag, text, '%s/p/1000words/3 ' % baseUrl)  
            with tag('li'):
               formatting.link(tag, text, '%s/p/100words/30 ' % baseUrl)                
         with tag('dl'):
            with tag('dt'):
               text('1000words')
            with tag('dd'):
               text('Choose personality traits from a list of 1000 words.')
            with tag('dt'):
               text('100words')
            with tag('dd'):
              text('Choose personality traits from a list of 100 words.')    
         with tag('p'):
               text('The following format varibles are supprted:')              
         with tag('dl'):
            with tag('dt'):
               text('html')
            with tag('dd'):
               text('Results formatted in html; best for human viewing.')
            with tag('dt'):
               text('text') 
            with tag('dd'):
               text('Plain text.  Looks ugly in browsers, but great for cut-n-paste.')
            with tag('dt'):
               text('htmlText')
            with tag('dd'):
               text('The same as text, but formatted so that it looks ok in html.')
            with tag('dt'):
               text('json')
            with tag('dd'):
               text('Your results, encoded as a list, ready for use by other programs.  '+
                    'You can think of this as the REST API for a personality service.')

         with tag('p'):
            with tag('b'):
               text('My Reuqest To Users')
         with tag('p'):
            text('Please send me feedback on the personality traits this web page gives you! '+
                 'You can send email to joshualevy2 @ hotmail dot com, or join the discussion '+
                 'on the CoTI software forum here: ')   
            formatting.link(tag, text, 'http://www.travellerrpg.com/CotI/Discuss/forumdisplay.php?f=63')
         with tag('p'):
            with tag('b'):
               text('Advice On Using This Website')
         with tag('p'):
            text('For NPCs, I think that the best way to generate a personality is to run this command:') 
         with tag('blockquote'):
            with tag('a', href='https://joshualevy.pythonanywhere.com/p/1000words/3'):
               text('https://joshualevy.pythonanywhere.com/p/1000words/3') 
         with tag('p'): 
            text("And then toss out any traits that don't fit, and arrage the rest in order of "+
                 "importance.  Most important first.  It's quick, easy, and I've found that it "+
                 "gives results which are both good and useful. If you find that you are tossing "+
                 "out more than 2 traits on average, then start out with 4 or more.  The goal is "+
                 "to end up with 2 or 3 good ones, in the order you like.")  
         with tag('p'):
            text('For PCs, the method above works ok, not great.  I prefer a different '+
                 'technique which is not supported yet, but will be soon.') 
      #   with tag('blockquote'):
      #      with tag('a', href='https://joshualevy.pythonanywhere.com/p/1000words/3'):
      #         text('https://joshualevy.pythonanywhere.com/p/1000words/3')   
      #   with tag('p'): 
      #      text("And then toss out any traits that don't fit, and arrage the rest in order of "+
      #           "importance, most important first.  It's quick, easy, and I've found that it "+
      #           "gives results which are both good and useful. If you find that you are tossing "+
      #           "out more than 2 traits on average, then start out with 4 or more.  The goal is "+
      #           "to end up with 2 or 3 good ones, in the order you like.") 
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