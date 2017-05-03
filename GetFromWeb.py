import json
import urllib.request

class GetFromWeb():

   sources = {
      # Danger! this one sometimes (not always) messes up encodings.
      'uinames': {'url': 'https://uinames.com/api/',
                  'type': 'spacesep',
                  'first': 'name',
                  'last': 'surname'},
      'names': {'url': 'https://randomuser.me/api/',
                'type': 'spacesep',
                'first':  'results.0.name.first',
                'last':  'results.0.name.last'},
      #'fakenames': {'url': 'api.namefake.com',
    #                'first': 'name',
    #                'last': ''}
   }

   @staticmethod
   def getDeepDict(top,names):   
      nameList = names.split('.')
      current = top       
      for name in nameList:       
         if type(current) == dict:
            current = current[name]
         elif type(current) == list:
            current = current[int(name)]             
      return current

   @staticmethod
   # raises KeyError if not there
   def getSource(name):
       return GetFromWeb.sources[name]

   @staticmethod
   def get(name):
      try:
         source = GetFromWeb.getSource(name)
      except KeyError as e:
         print('GetFromWeb has no entry for your source: %s' % name)
         raise e

      request = urllib.request.Request( source['url'])     
      response = urllib.request.urlopen(request)     
      encoding = response.headers.get_content_charset()    
      #print(encoding)
      # if no encoding provided, then we guess.
      if encoding is None:          
         content = response.read()              
      else:
         content = response.read().decode(encoding)
         
      #print(content) 
      result = json.loads(content)      
      #print(result)
      try:    
         retType = source['type']
         if retType == 'raw':
            return result
         elif retType == 'spacesep':
            
            return ('%s %s' % 
                    (GetFromWeb.getDeepDict(result,source['first']),
                     GetFromWeb.getDeepDict(result,source['last'])))
         else:
            print("Unknown type field (%s) in the %s record" % (retType,name))
            return None
      except:
         print("No type field in the %s record" % name)
         return None

# if no arguments, test a little bit.
if __name__ == '__main__':
   for ii in range(5):
      s = GetFromWeb.get('names')
      print(s)
   for ii in range(5):      
      s = GetFromWeb.get('uinames')
      print(s)
        

