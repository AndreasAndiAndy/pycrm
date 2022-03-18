import i18n
import xml.etree.ElementTree as ET

from os.path import exists

######################
#Globale Funkton i18n
#####################
def _(str):

    LOCALE = i18n.getLocale() 
    t = Translator.getInstance(LOCALE)

    res = ""
    
    if str in t.keys(): 
        res = t[str]
    
    else:
        res = str
    
    
    return res
    
class Translator:
   __instance = None

   
   @staticmethod 
   def getInstance(loc):
   
      if Translator.__instance == None:
         Translator()
         
      dictionary = {}   
        
      filename = "i18n" + "/" + loc + ".xml"
    
      if not exists(filename):
        return dictionary

      else:    
        tree = ET.ElementTree(file=filename)
        root = tree.getroot()

        inputs = []
        outputs = []

        for str in root.iter('string'):
            for child in str:
                if child.tag == "input":
                    inputs.append(child.text)
                if child.tag == "output":
                    outputs.append(child.text)
                
        for i in range(0, len(inputs)):
            dictionary[inputs[i]] = outputs[i]


      #return Translator.__instance
      
      return dictionary
            
   def __init__(self):
   
      if Translator.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         Translator.__instance = self
