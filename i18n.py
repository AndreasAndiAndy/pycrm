import dbaccess

def getLocale():

    loc = dbaccess.getLocale()
    
    if loc == None:
        return "de_DE"
        
    else:
        return loc
    


def setLocale(l):
    
    if l == "Deutsch":
        l = "de_DE"
        
    if l == "English":
        l = "en_GB"
    
    dbaccess.setLocale(l)


