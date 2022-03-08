################################

#Author: Andreas Gölz

#This document is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License, version 3, 
#as published by the Free Software Foundation. 

################################

from distutils.command.check import check

################################

import sqlite3

def insertReadListFromFile(conn, legenda, cat):
    
    if cat == "appointments":
        cur = conn.cursor()
        for l in legenda:
            datum = l.split(",")[0].strip()
            name = l.split(",")[1].strip()
            desc = l.split(",")[2].strip()
            enddatum = l.split(",")[3].strip()      
    
            if len(name) <1:
                name = "Neuer Termin!"
    
            if len(desc) < 1:
                desc = ''
    
            cur.execute("INSERT INTO appointment (datum, termin, description, enddatum) VALUES(?, ?, ?, ?)", (datum, name, desc, enddatum,)) 
            conn.commit()
           
        cur.close()
    
    
    if cat == "rescon":
        cur = conn.cursor()
        
        for l in legenda:
           
           tel = l.split(",")[0].strip()
           mobil = l.split(",")[1].strip()
           email = l.split(",")[2].strip()
           str = l.split(",")[3].strip()
           hnr = l.split(",")[4].strip()
           plz = l.split(",")[5].strip()
           ort = l.split(",")[6].strip()
           gebtag = l.split(",")[7].strip()
           name = l.split(",")[8].strip()
           iban = l.split(",")[9].strip()
           bic = l.split(",")[10].strip()
        
           cur.execute("INSERT INTO cres (tel, mobil, email, street, num, plz, ort, birthday, datum, name, iban, bic) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (tel, mobil, email, str, hnr, plz, ort, gebtag, "0000-00-00 00:00", name, iban, bic,)) 
           conn.commit()
           
        cur.close()





def doQueryDeleteAppointmentsAndCres2(conn):
    cur = conn.cursor()
    cur.execute("DELETE FROM appointment")
    cur.execute("DELETE FROM cres WHERE datum <> ?", ('0000-00-00 00:00', ))
    conn.commit()
    cur.close()


def insertDictAddenda(conn, rcDict):
    cur = conn.cursor() 
    
    for name, isdelete in rcDict.items():        
        cur.execute("INSERT INTO addenda (name, date, isdelete) VALUES(?, ?, ?)", (name, "0000-00-00 00:00", isdelete,))   
        conn.commit()
    
    cur.close()


def doQueryInsertWithTitleAndDescription2(conn, monthlies, ttitel, tbeschreibung, uhrzeit_end):
    cur = conn.cursor() 
    
    for datum in monthlies:
        e = datum.split(" ")[0] + " " + uhrzeit_end
        cur.execute("INSERT INTO appointment (datum, termin, description, enddatum) VALUES(?, ?, ?, ?)", (datum, ttitel, tbeschreibung, e,))
    
    conn.commit()
    cur.close()

def doQueryDel2(conn, datum):
    cur = conn.cursor()
    cur.execute("DELETE FROM appointment WHERE datum = ?", (datum,))
    conn.commit()
    cur.close()

def deleteCres2Date(conn, datum):
    cur = conn.cursor()
    cur.execute("DELETE FROM cres WHERE datum = ?", (datum,))
    conn.commit()
    cur.close()

def doQueryResContacts2(conn, isChecked, datum):
    result = {}
    cur = conn.cursor()  
    if isChecked:
        cur.execute("SELECT name, cres.datum FROM cres INNER JOIN appointment ON cres.datum = appointment.datum AND cres.datum = ?", (datum, ))
        for datum, name in cur.fetchall():
            result[datum] = name
    
    else:
        cur.execute("SELECT name, cres.datum FROM cres INNER JOIN appointment ON cres.datum = appointment.datum AND cres.datum != ?", (datum, ))
        for datum, name in cur.fetchall():
            result[datum] = name     
    conn.commit()
    
    if not isChecked:
        cur.execute("SELECT name, cres.datum FROM cres WHERE datum = ?", ("0000-00-00 00:00", ))
        for datum, name in cur.fetchall():
            result[datum] = name
    
    conn.commit()
    cur.close()
    return result

def doQueryCrsFor(conn, name):
    result = []
    cur = conn.cursor()
    cur.execute("SELECT * FROM cres WHERE name = ? AND datum = ?", (name, "0000-00-00 00:00",))
    for x in cur.fetchall():
        result.append(x)
    conn.commit()
    cur.close()
    return result 

def insertCres2(conn, name, date):
    
    date = date[0:16]
    
    cres = doQueryCrsFor(conn, name)[0]
    cresentry = []
    
    for x in cres:
        cresentry.append(x)
       
    cresentry[8] = date
    
    cur = conn.cursor()
    cur.execute("INSERT INTO cres (tel, mobil, email, street, num, plz, ort, birthday, datum, name, iban, bic) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (cresentry[0], cresentry[1], cresentry[2], cresentry[3], cresentry[4], cresentry[5], cresentry[6], cresentry[7], cresentry[8], cresentry[9], cresentry[10], cresentry[11],))
    conn.commit()
    cur.close()

def doQueryRC2(conn):
    result = []
    cur = conn.cursor()
    cur.execute("SELECT * FROM cres WHERE datum = ?", ("0000-00-00 00:00",))
    for x in cur.fetchall():
        result.append(x)
    conn.commit()
    cur.close()
    return result    

def insertCres(conn, name, date):
    cres = doQueryCrsFor(conn, name)[0]
    cresentry = []
    
    for x in cres:
        cresentry.append(x)
       
    cresentry[8] = date
    
    cur = conn.cursor()
    cur.execute("INSERT INTO cres (tel, mobil, email, street, num, plz, ort, birthday, datum, name, iban, bic) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (cresentry[0], cresentry[1], cresentry[2], cresentry[3], cresentry[4], cresentry[5], cresentry[6], cresentry[7], cresentry[8], cresentry[9], cresentry[10], cresentry[11],))
    conn.commit()
    cur.close()



def doQueryRCWith(conn):
    ds = []
    cur = conn.cursor()
    cur.execute("SELECT name FROM cres WHERE datum = ?", ("0000-00-00 00:00",))
    for d in cur.fetchall():
        ds.append(d)
    conn.commit()
    cur.close()
    return ds    

def doQueryCategories(conn):
    categories = []
    cur = conn.cursor()
    cur.execute("SELECT cat FROM categories")
    for cat in cur.fetchall():
        categories.append(cat)
    return categories   

def insertCresFullData(conn, tel, mobil,  email,  str, hnr,  plz,  ort,  gebtag,  name,  iban,  bic,  cattosave):
    cur = conn.cursor()
    resourcecontact = doQueryRCWith(conn)
    isresourcecontactcorrect = True
    
    for x in resourcecontact:
        if x[0] == name:
            isresourcecontactcorrect = False
    
    if isresourcecontactcorrect:    
        sql = "INSERT INTO cres (tel, mobil, email, street, num, plz, ort, birthday, datum, name, iban, bic) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = tel, mobil,  email,  str, hnr,  plz,  ort,  gebtag, "0000-00-00 00:00",  name,  iban,  bic        
        cur.execute(sql, val)    
    
    iscategorycorrect = True
    if len(cattosave) > 0:
        cats = doQueryCategories(conn)
        for x in cats:
            if cattosave == x[0]:
                iscategorycorrect = False
 
    conn.commit()
    cur.close()   
    cur = conn.cursor()
    
    if iscategorycorrect and cattosave != '':
        cur.execute("INSERT INTO categories (cat) VALUES(?)", (cattosave,))
    
    conn.commit() 
    cur.close()

def doQuery(conn):
    appntments = {}
    cur = conn.cursor()
    cur.execute("SELECT datum, termin FROM appointment ORDER BY datum")
    for date, appointment in cur.fetchall():
        appntments[date] = appointment
    return appntments    


def doQueryRCFILTERED(conn, filter_text):
    result = []        
    cur = conn.cursor()
    name = f'%{filter_text}%'
    cur.execute("SELECT * FROM cres WHERE datum = ? AND name ILIKE ?", ("0000-00-00 00:00", name))
    for x in cur.fetchall():
        result.append(x)
    conn.commit()
    cur.close()
    return result    


def doQueryRC(conn):
    result = []
    cur = conn.cursor()
    cur.execute("SELECT * FROM cres WHERE datum = ?", ("0000-00-00 00:00",))
    for x in cur.fetchall():
        result.append(x)
    conn.commit()
    cur.close()
    return result    


def doQueryDescriptionFor(conn, datum):
    result = []
    cur = conn.cursor()
    cur.execute("SELECT description FROM appointment WHERE datum = ?", (datum, ))
    for x in cur.fetchall():
        result.append(x)
    conn.commit()
    cur.close()
    return result    

def doQueryNameFor(conn, datum):
    result = []
    cur = conn.cursor()
    cur.execute("SELECT termin FROM appointment WHERE datum = ?", (datum, ))
    for x in cur.fetchall():
        result.append(x)
    conn.commit()
    cur.close()
    return result    

def doQueryResContacts(conn, isChecked, datum):
    result = {}
    cur = conn.cursor()  
    if isChecked:
        cur.execute("SELECT name, cres.datum FROM cres INNER JOIN appointment ON cres.datum = appointment.datum AND cres.datum = ?", (datum, ))
        for datum, name in cur.fetchall():
            result[datum] = name
    
    else:
        cur.execute("SELECT name, cres.datum FROM cres INNER JOIN appointment ON cres.datum = appointment.datum AND cres.datum != ?", (datum, ))
        for datum, name in cur.fetchall():
            result[datum] = name     
    conn.commit()
    
    if not isChecked:
        cur.execute("SELECT name, cres.datum FROM cres WHERE datum = ?", ("0000-00-00 00:00", ))
        for datum, name in cur.fetchall():
            result[datum] = name
    
    conn.commit()
    cur.close()
    return result
 

def doQueryUpdate(conn, dateinput, name, beschr, u):
    cur = conn.cursor()
    cur.execute("UPDATE appointment SET datum = ?, termin = ?, description = ? WHERE datum = ? ", (u, name, beschr, dateinput,))
    conn.commit()
    cur.close()
 

def updateMainFilter(conn, fltrstring):  
    cur = conn.cursor()
    cur.execute("UPDATE auxiliaries SET filterstring = ?", (fltrstring,))
    conn.commit()
    cur.close()
  
def updateCresForCols(conn, d):
    cur = conn.cursor()
    cur.execute("UPDATE cres SET tel = ?, mobil = ?, email = ?, street = ?, num = ?, plz = ?, ort = ?, birthday = ?, iban = ?, bic = ? WHERE name = ? ", (d["tel"], d["mobil"], d["email"], d["street"], d["num"], d["plz"], d["ort"], d["birthday"], d["iban"], d["bic"], d["name"],))
    conn.commit()
    cur.close()

def doQueryEnddates(conn):
    enddates = {}
    cur = conn.cursor()
    cur.execute("SELECT datum, enddatum FROM appointment")
    for datum, enddatum in cur.fetchall():
        enddates[datum] = enddatum
    return enddates    
    
    
def deleteAllCres(conn):    
    cur = conn.cursor()
    cur.execute("DELETE FROM cres")
    cur.execute("DELETE FROM categories")
    conn.commit()
    cur.close()
    
def deleteCres(conn, name, date):
    cur = conn.cursor()
    cur.execute("DELETE FROM cres WHERE datum = ? AND name = ?", (date, name,))
    conn.commit()
    cur.close()

def doQueryDel(conn, datum):
    cur = conn.cursor()
    cur.execute("DELETE FROM appointment WHERE datum = ?", (datum,))
    conn.commit()
    cur.close()

def deleteResContactsForNameIfFalse(conn, d):
    delenda = []    
    cur = conn.cursor()  
    for name, checked in d.items():
        if check:
            delenda.append(name)

    for delendum in delenda:
        cur.execute("DELETE FROM cres WHERE name = ?", (delendum,))
        conn.commit()
    cur.close()
  

def doQueryNameFor2(conn, datum):
    result = []
    cur = conn.cursor()
    cur.execute("SELECT termin FROM appointment WHERE datum = ?", (datum, ))
    for x in cur.fetchall():
        result.append(x)
    conn.commit()
    cur.close()
    return result    

def doQueryUpdate2WithEnd(conn, dateinput, name, beschr, u, end_date):
    cur = conn.cursor()
     
    cur.execute("UPDATE appointment SET datum = ?, termin = ?, description = ?, enddatum = ? WHERE datum = ? ", (u, name, beschr, end_date, dateinput,))
    conn.commit()
    cur.close()

def doQueryUpdate2(conn, dateinput, name, beschr, u):
    cur = conn.cursor()    
    cur.execute("UPDATE appointment SET datum = ?, termin = ?, description = ? WHERE datum = ? ", (u, name, beschr, dateinput,))
    conn.commit()
    cur.close()

def doQueryRCWith2(conn):
    ds = []
    cur = conn.cursor()
    cur.execute("SELECT name FROM cres WHERE datum = ?", ("0000-00-00 00:00",))
    for d in cur.fetchall():
        ds.append(d)
    conn.commit()
    cur.close()
    return ds    

def doQueryInsertIntoSettingsPath(conn, p):
    cur = conn.cursor()
    cur.execute("INSERT INTO settings (path) VALUES(?)", (p,))
    conn.commit() 
    cur.close()


def insertCresFullData2(conn, tel, mobil,  email,  str, hnr,  plz,  ort,  gebtag,  name,  iban,  bic,  cattosave):
    cur = conn.cursor()
    resourcecontact = doQueryRCWith2(conn)
    isresourcecontactcorrect = True
    
    for x in resourcecontact:
        if x[0] == name:
            isresourcecontactcorrect = False
    
    if isresourcecontactcorrect:
        sql = "INSERT INTO cres (tel, mobil, email, street, num, plz, ort, birthday, datum, name, iban, bic) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = tel, mobil,  email,  str, hnr,  plz,  ort,  gebtag, "0000-00-00 00:00",  name,  iban,  bic        
        cur.execute(sql, val)    
    
    iscategorycorrect = True
    if len(cattosave) > 0:
        cats = doQueryCategories2(conn)
        for x in cats:
            if cattosave == x[0]:
                iscategorycorrect = False
 
    conn.commit()
    cur.close()   
    cur = conn.cursor()
    
    if iscategorycorrect and cattosave != '':
        cur.execute("INSERT INTO categories (cat) VALUES(?)", (cattosave,))
    
    conn.commit() 
    cur.close()

def doQueryDescriptionFor2(conn, datum):
    result = []
    cur = conn.cursor()
    cur.execute("SELECT description FROM appointment WHERE datum = ?", (datum, ))
    for x in cur.fetchall():
        result.append(x)
    conn.commit()
    cur.close()
    return result    

def doQueryCategories2(conn):
    categories = []
    cur = conn.cursor()
    cur.execute("SELECT cat FROM categories")
    for cat in cur.fetchall():
        categories.append(cat)
    return categories    


def doQueryRCFILTERED2(conn, filter_text):
    result = []        
    cur = conn.cursor()
    name = f'%{filter_text}%'
    cur.execute("SELECT * FROM cres WHERE datum = ? AND name LIKE ?", ("0000-00-00 00:00", name))
    
    for x in cur.fetchall():
        result.append(x)
    conn.commit()
    cur.close()
    return result    


def deleteCres2(conn, name, date):
    cur = conn.cursor()
    cur.execute("DELETE FROM cres WHERE datum = ? AND name = ?", (date, name,))
    conn.commit()
    cur.close()

def updateCresForCols2(conn, d):
    cur = conn.cursor()
    cur.execute("UPDATE cres SET tel = ?, mobil = ?, email = ?, street = ?, num = ?, plz = ?, ort = ?, birthday = ?, iban = ?, bic = ? WHERE name = ? ", (d["tel"], d["mobil"], d["email"], d["street"], d["num"], d["plz"], d["ort"], d["birthday"], d["iban"], d["bic"], d["name"],))
    conn.commit()
    cur.close()


def deleteResContactsForNameIfFalse2(conn, d):
    delenda = []    
    cur = conn.cursor()  
    for name, checked in d.items():
        if check:
            delenda.append(name)

    for delendum in delenda:
        cur.execute("DELETE FROM cres WHERE name = ?", (delendum,))
        conn.commit()
    cur.close()

def updateMainFilter2(conn, fltrstring):  
    cur = conn.cursor()
    cur.execute("UPDATE auxiliaries SET filterstring = ?", (fltrstring,))
    conn.commit()
    cur.close()

def doQueryFilterText(conn):
    result = []
    cur = conn.cursor()
    cur.execute("SELECT * FROM auxiliaries")
    for x in cur.fetchall():
        result.append(x)
    conn.commit()
    cur.close()

    if len(result) == 0:
        updateMainFilter2(conn, "")
        cur = conn.cursor()
        cur.execute("INSERT INTO auxiliaries (filterstring) VALUES(?)", ("",))
        conn.commit()
        cur.close()
        result = [('',)]

    return result    


def doQueryPath(conn):
    result = []
    cur = conn.cursor()
    cur.execute("SELECT path FROM settings")
    for x in cur.fetchall():
        result.append(x)
    conn.commit()
    cur.close()
    return result 

def doQueryDeleteSeries(conn,nly):
    cur = conn.cursor()
    for n in nly:
        cur.execute("DELETE FROM appointment WHERE datum = ?", (n, ))
        cur.execute("DELETE FROM cres WHERE datum = ?", (n, ))
        conn.commit()

    cur.close()


def doQueryEditAppointmentAndCres(conn, ttitel, tbeschreibung, termin_alt, date):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM cres WHERE datum = ?", (termin_alt,))
    numCres = int(cur.fetchall()[0][0])
    
    if numCres > 0:
        cur.execute("UPDATE cres SET datum = ? WHERE datum = ? ", (date, termin_alt,))
    
    doQueryUpdate2(conn, termin_alt, ttitel, tbeschreibung, date)
    
    conn.commit()
    cur.close()


def doQueryInsertPath(conn, path):
    result = []
    cur = conn.cursor()
    cur.execute("SELECT path FROM settings")
    for x in cur.fetchall():
        result.append(x)
    conn.commit()
    cur.close()

    if len(result) == 0:
        cur = conn.cursor()
        cur.execute("INSERT INTO settings (path) VALUES(?)", (path,))
        conn.commit()
        cur.close()

    else:    
        cur = conn.cursor()
        cur.execute("UPDATE settings SET path = ?", (path,))
        conn.commit()
        cur.close()

def doQueryInsert2(conn, datum, ttitel, tbeschreibung, dateinput_end):
    cur = conn.cursor()
    cur.execute("INSERT INTO appointment (datum, termin, description, enddatum) VALUES(?, ?, ?, ?)", (datum, ttitel, tbeschreibung, dateinput_end))
    conn.commit()
    cur.close()

def doQuery2(conn):
    appntments = {}
    cur = conn.cursor()
    cur.execute("SELECT datum, termin FROM appointment ORDER BY datum")
    for date, appointment in cur.fetchall():
        appntments[date] = appointment
    return appntments    

def filterText():
    myConnection = sqlite3.connect("pcrm.db")
    res = doQueryFilterText(myConnection)
    return res

def insertAppointment(datum, ttitel, tbeschreibung, dateinput_end): 
    myConnection = sqlite3.connect("pcrm.db")
    doQueryInsert2(myConnection, datum, ttitel, tbeschreibung, dateinput_end)   
    
def allAppointments():
    myConnection = sqlite3.connect("pcrm.db")
    res = doQuery2(myConnection)    
    return res    

def updateMainFilterString(fltrstring):
    myConnection = sqlite3.connect("pcrm.db")
    updateMainFilter2(myConnection, fltrstring)
    
def allRC():
    myConnection = sqlite3.connect("pcrm.db")
    res = doQueryRC2(myConnection)    
    return res          

def deleteRCs(d):
    myConnection = sqlite3.connect("pcrm.db")
    deleteResContactsForNameIfFalse2(myConnection, d) 
   
def doQueryCategoriesAll(conn, cat):
    infos = []
    cur = conn.cursor()
    cur.execute("SELECT * FROM cres WHERE name = ? AND datum = ?", (cat, '0000-00-00 00:00', )) 
    for cresinfo in cur.fetchall():
        infos.append(cresinfo[0])
        infos.append(cresinfo[1])
        infos.append(cresinfo[2])
        infos.append(cresinfo[3])
        infos.append(cresinfo[4])
        infos.append(cresinfo[5])
        infos.append(cresinfo[6])
        infos.append(cresinfo[7])
        infos.append(cresinfo[10])
        infos.append(cresinfo[11])
    return infos       
    
def allCategoriesAll(cat):    
    myConnection = sqlite3.connect("pcrm.db")
    res = doQueryCategoriesAll(myConnection, cat)    
    return res
    
def updateCres2(creasnewcols):
    myConnection = sqlite3.connect("pcrm.db")
    colsdict = {}   
    statusquo = doQueryCategoriesAll(myConnection, creasnewcols["NAME"])
    
    colsdict["tel"] = statusquo[0]
    colsdict["mobil"] = statusquo[1]
    colsdict["email"] = statusquo[2] 
    colsdict["street"] = statusquo[3]
    colsdict["num"] = statusquo[4]
    colsdict["plz"] = statusquo[5]
    colsdict["ort"] = statusquo[6]
    colsdict["birthday"] = statusquo[7]
    colsdict["iban"] = statusquo[8]
    colsdict["bic"] = statusquo[9]
    colsdict["name"] = ""
    
    for col in creasnewcols:
         if col == "TEL":
            colsdict["tel"] = creasnewcols[col]
        
         if col == "MOBIL":
             colsdict["mobil"] = creasnewcols[col]
    
         if col == "EMAIL":
             colsdict["email"] = creasnewcols[col]  
    
         if col == "STR":
             colsdict["street"] = creasnewcols[col]
    
         if col == "NUM":
             colsdict["num"] = creasnewcols[col]
   
         if col == "PLZ":
             colsdict["plz"] = creasnewcols[col]
            
         if col == "ORT":
             colsdict["ort"] = creasnewcols[col]
    
         if col == "GEB":
             colsdict["birthday"] = creasnewcols[col]
    
         if col == "IBAN":
             colsdict["iban"] = creasnewcols[col]
            
         if col == "BIC":
             colsdict["bic"] = creasnewcols[col]
    
         if col == "NAME":
             colsdict["name"] = creasnewcols[col]
    
    updateCresForCols2(myConnection, colsdict)     
       
def insertIntoCresWith(name, date):
    myConnection = sqlite3.connect("pcrm.db")
    insertCres2(myConnection, name, date)    
    
def deleteFromCresWith(name, date):
    myConnection = sqlite3.connect("pcrm.db")
    deleteCres2(myConnection, name, date)


def getUncheckedResContactsFor2(d):
    myConnection = sqlite3.connect("pcrm.db")
    res = doQueryResContacts2(myConnection, False, d)
    return res

def getCheckedResContactsFor2(d):
    myConnection = sqlite3.connect("pcrm.db")
    res = doQueryResContacts2(myConnection, True, d) 
    return res

def allRCFilteredBy(filterText):
    myConnection = sqlite3.connect("pcrm.db")
    res = doQueryRCFILTERED2(myConnection, filterText)
    return res

def allCategories2():    
    myConnection = sqlite3.connect("pcrm.db")
    res = doQueryCategories2(myConnection)    
    return res

def selectDescriptionFor2(datum):
    myConnection = sqlite3.connect("pcrm.db")
    res = doQueryDescriptionFor2(myConnection, datum)    
    return res

def insertNewRC2(tel, mobil,  email,  str, hnr,  plz,  ort,  gebtag,  name,  iban,  bic,  cattosave):
    myConnection = sqlite3.connect("pcrm.db")
    insertCresFullData2(myConnection, tel, mobil,  email,  str, hnr,  plz,  ort,  gebtag,  name,  iban,  bic,  cattosave)

def editAppointmentDateUpdate2(title, description, dateinput, dateinput_end):
        myConnection = sqlite3.connect("pcrm.db")
        doQueryUpdate2WithEnd(myConnection, dateinput, title, description, dateinput, dateinput_end)

def updateAppointment2(dateinput, name_beschr_u):
    myConnection = sqlite3.connect("pcrm.db")
    doQueryUpdate2(myConnection, dateinput, name_beschr_u[0], name_beschr_u[1], name_beschr_u[2])
    
def deleteAppointment2(datum):
    myConnection = sqlite3.connect("pcrm.db")
    deleteCres2Date(myConnection, datum)
    doQueryDel2(myConnection, datum)

def insertAppointmentWithTitleAndDescription2(nthlies, ttitel, tbeschreibung, uhrzeit_end):
    myConnection = sqlite3.connect("pcrm.db")
    doQueryInsertWithTitleAndDescription2(myConnection, nthlies, ttitel, tbeschreibung, uhrzeit_end)
    
def selectNameFor2(datum):
    myConnection = sqlite3.connect("pcrm.db")
    res = doQueryNameFor(myConnection, datum)    
    return res

def selectFromSettings():
    myConnection = sqlite3.connect("pcrm.db")
    res = doQueryPath(myConnection)   
    return res

def editAppointment(ttitel, tbeschreibung, termin_alt, date):
    myConnection = sqlite3.connect("pcrm.db")
    doQueryEditAppointmentAndCres(myConnection, ttitel, tbeschreibung, termin_alt, date)

def allEnddates():
    myConnection = sqlite3.connect("pcrm.db")
    res = doQueryEnddates(myConnection)
    return res

def insertIntoSettings(path):
    myConnection = sqlite3.connect("pcrm.db")
    doQueryInsertPath(myConnection, path)
    
def deleteFromAppointmentsAndCRes():
    myConnection = sqlite3.connect("pcrm.db")    
    doQueryDeleteAppointmentsAndCres2(myConnection)
    
def readListFromFile(legenda, cat):
    myConnection = sqlite3.connect("pcrm.db") 
    insertReadListFromFile(myConnection, legenda, cat)      
    
def deleteAllRCs():   
    myConnection = sqlite3.connect("pcrm.db")    
    deleteAllCres(myConnection) 
    

def insertTitleAndDates(rcDict):  
    myConnection = sqlite3.connect("pcrm.db")    
    insertDictAddenda(myConnection, rcDict)
    
    
def deleteSeries(nly):
    myConnection = sqlite3.connect("pcrm.db")
    doQueryDeleteSeries(myConnection,nly)
    
    
def insertIntoSettingsPath(p):
    myConnection = sqlite3.connect("pcrm.db")
    doQueryInsertIntoSettingsPath(myConnection,p)

    
    
##########################################################################################################

def updateCresSerial(conn, cresentry, date):
    
    rc_tuple = cresentry[0]
    
    d = {}
    
    d["tel"] = rc_tuple[0] 
    d["mobil"] = rc_tuple[1] 
    d["email"] = rc_tuple[2]
    d["street"] = rc_tuple[3]
    d["num"] = rc_tuple[4]
    d["plz"] = rc_tuple[5]
    d["ort"] = rc_tuple[6]
    d["birthday"] = rc_tuple[7]
    d["date"] = date
    d["name"] = rc_tuple[9]
    d["iban"] = rc_tuple[10]
    d["bic"] = rc_tuple[11]
    
    cur = conn.cursor()
    cur.execute("INSERT INTO cres (tel, mobil, email, street, num, plz, ort, birthday, datum, name, iban, bic) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (d["tel"], d["mobil"], d["email"], d["street"], d["num"], d["plz"], d["ort"], d["birthday"], d["date"], d["name"],d["iban"], d["bic"],))
    conn.commit()
    cur.close()

def connectResourceContacts(thedts):
    dict = {}
    
    conn = sqlite3.connect("pcrm.db")    
    cur = conn.cursor()
    
    cur.execute("SELECT name, isdelete FROM addenda WHERE date = ?", ("0000-00-00 00:00",))
    
    res = []
    for name, isdelete in cur.fetchall():
        if isdelete == "0":
            res.append(name)   
    conn.commit()
    cur.close()
    
    for d in thedts:
        dict[d] = res
    
    conn = sqlite3.connect("pcrm.db")    
    cur = conn.cursor()
    cur.execute("DELETE FROM addenda WHERE isdelete = ?", ("False",))
    conn.commit()
    cur.close()
    
    #Anhand der Namen die Reskontakte aus cres holen und mit den Schlüsseln in die cres-Datenbank setzen.

    conn = sqlite3.connect("pcrm.db")    
    cur = conn.cursor()
    
    for date, rclist in dict.items():
         
        for rc in rclist:
            
            cur.execute("SELECT * FROM cres WHERE name = ? AND datum = ?", (rc, '0000-00-00 00:00',))
            
            result = []
            for x in cur.fetchall():
                result.append(x)
            
            updateCresSerial(conn, result, date)
            
            conn.commit()

    cur.close()
