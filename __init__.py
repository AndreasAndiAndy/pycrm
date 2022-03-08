################################

#Author: Andreas Gölz

#This document is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License, version 3, 
#as published by the Free Software Foundation. 

###############################

import os
import sys
import re
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import *
from PyQt5 import *
from functools import partial
import dbaccess, validators, filereader
from ctypes.test.test_pickling import name
from datetime import timedelta
from tkinter import *
from tkinter.filedialog import askdirectory, askopenfilename
from test.test_decimal import directory


 
#Die Ressourcenkontakte können hier hinzugefügt oder bearbeitet werden.
class ScrollMessageBoxShowResourceContactsAdd(QMessageBox):  

   def __init__(self, *args, **kwargs):
       
       def msgbtn(tf, btn):
           
           if btn.text().upper() == 'CANCEL':
               #Hier in die DB schreiben, dann das Ding neu aufrufen.  
               dbaccess.updateMainFilterString("")            
               self.close()

           if btn.text().upper() == 'OK':
               #Hier in die DB schreiben, dann das Ding neu aufrufen. 
               dbaccess.updateMainFilterString(tf.text())
               self.close()
               result = ScrollMessageBoxShowResourceContactsAdd(None)
               result.exec_()
       
           if not (btn.text().upper() == 'OK' or btn.text().upper() == 'CANCEL'):
               sys.exit(self.exec_())
       
       QMessageBox.__init__(self, *args, **kwargs)
       
       self.setWindowTitle("Ressourcenkontakte einsehen oder hinzufügen.")
       
       self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

       self.setInformativeText("Filtern: OK drücken. ~~~~ Hinzufügen: Häkchen setzen, dann 'CANCEL'")
       
       filtertf = QLineEdit() 
       filtertf.setStyleSheet("background-color: yellow; max-height: 2em; max-width: 22em;");
       self.buttonClicked.connect(partial(msgbtn, filtertf))
       
       scroll = QScrollArea(self)
       scroll.setWidgetResizable(True)
       
       self.content = QWidget()
       
       scroll.setWidget(self.content)
       
       lay = QVBoxLayout(self.content)
       
       self.addendaDict = {} 
       self.addDict = {}
       
       filterText = dbaccess.filterText()[0][0]
       
       filtertf.setText(filterText)
       
       if filterText == "":
           for rc in dbaccess.allRC(): 
               addCB = QCheckBox('add', self)
               addCB.stateChanged.connect(partial(self.btnstateAdd, addCB, self.addendaDict))
               addCB.setObjectName(rc[9])
 
               qb = QPushButton(rc[9], self)
               qb.released.connect(partial(self.button_releasedRC, rc[9]))
               lay.addWidget(qb)
               lay.addWidget(addCB)
 
       else:
           for rc in dbaccess.allRCFilteredBy(filterText): 
               addCB = QCheckBox('add', self)
               addCB.stateChanged.connect(partial(self.btnstateAdd, addCB, self.addendaDict))
               addCB.setObjectName(rc[9])
 
               qb = QPushButton(rc[9], self)
               qb.released.connect(partial(self.button_releasedRC, rc[9]))
               lay.addWidget(qb)
               lay.addWidget(addCB)
 
       lay.addWidget(filtertf) 
       
       self.buttonClicked.connect(self.msgButtonClickDel)   
       self.layout().addWidget(scroll, 0, 0, 1, self.layout().columnCount())
       self.setStyleSheet("QScrollArea{min-width:410 px; min-height: 600px}")

   def btnstateAdd(self, dlt, dlts):    
       dlts[dlt.objectName()] = True
       if dlt.isChecked:
           dlts[dlt.objectName()] = False
       self.addDict = dlts

   def msgButtonClickDel(self, i):
       if i.text().upper() == "CANCEL":
           dbaccess.insertTitleAndDates(self.addendaDict)
           self.addendaDict = {}

   def button_releasedRC(self, nameshow):
       ScrollMessageBoxRCInfo(QMessageBox.Information, nameshow, '')


#Die Ressourcenkontakte können hier gelöscht oder bearbeitet werden.
class ScrollMessageBoxShowResourceContacts(QMessageBox):  

   def __init__(self, *args, **kwargs):
       
       def msgbtn(tf, btn):
           
           if btn.text().upper() == 'CANCEL':
               #Hier in die DB schreiben, dann das Ding neu aufrufen. # 
               dbaccess.updateMainFilterString("")            
               self.close()

           if btn.text().upper() == 'OK':
               #Hier in die DB schreiben, dann das Ding neu aufrufen. #
               dbaccess.updateMainFilterString(tf.text())
               self.close()
               result = ScrollMessageBoxShowResourceContacts(None)
               result.exec_()
       
           if not (btn.text().upper() == 'OK' or btn.text().upper() == 'CANCEL'):
               sys.exit(self.exec_())
       
       QMessageBox.__init__(self, *args, **kwargs)
       
       self.setWindowTitle("Ressourcenkontakte einsehen oder löschen.")
       
       self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

       self.setInformativeText("Filtern: OK drücken. ~~~~ Löschen: Häkchen setzen, dann 'CANCEL'")
       
       filtertf = QLineEdit() 
       filtertf.setStyleSheet("background-color: yellow; max-height: 2em; max-width: 22em;");
       self.buttonClicked.connect(partial(msgbtn, filtertf))
       
       scroll = QScrollArea(self)
       scroll.setWidgetResizable(True)
       
       self.content = QWidget()
       
       scroll.setWidget(self.content)
       
       lay = QVBoxLayout(self.content)
       
       delendaDict = {} 
       self.delDict = {}
       
       filterText = dbaccess.filterText()[0][0]
       
       filtertf.setText(filterText)
       
       if filterText == "":
           for rc in dbaccess.allRC(): 
               deleteCB = QCheckBox('delete', self)
               deleteCB.stateChanged.connect(partial(self.btnstateDel, deleteCB, delendaDict))
               deleteCB.setObjectName(rc[9])
 
               qb = QPushButton(rc[9], self)
               qb.released.connect(partial(self.button_releasedRC, rc[9]))
               lay.addWidget(qb)
               lay.addWidget(deleteCB)
 
       else:
           for rc in dbaccess.allRCFilteredBy(filterText): 
               deleteCB = QCheckBox('delete', self)
               deleteCB.stateChanged.connect(partial(self.btnstateDel, deleteCB, delendaDict))
               deleteCB.setObjectName(rc[9])
 
               qb = QPushButton(rc[9], self)
               qb.released.connect(partial(self.button_releasedRC, rc[9]))
               lay.addWidget(qb)
               lay.addWidget(deleteCB)
 
       lay.addWidget(filtertf) 
 
       delete_all_rc = QPushButton('Alle Ressourcenkontakte löschen', self)
       delete_all_rc.released.connect(partial(self.button_releasedDeAllRC))
       lay.addWidget(delete_all_rc)
       
       self.buttonClicked.connect(self.msgButtonClickDel)   
       self.layout().addWidget(scroll, 0, 0, 1, self.layout().columnCount())
       self.setStyleSheet("QScrollArea{min-width:410 px; min-height: 600px}")

   def btnstateDel(self, dlt, dlts):    
       dlts[dlt.objectName()] = False
       if dlt.isChecked:
           dlts[dlt.objectName()] = True
       self.delDict = dlts

   def msgButtonClickDel(self, i):
       if i.text().upper() == "CANCEL":
           dbaccess.deleteRCs(self.delDict) 

   def button_releasedRC(self, nameshow):
       ScrollMessageBoxRCInfo(QMessageBox.Information, nameshow, '')

   def button_releasedDeAllRC(self):
       dbaccess.deleteAllRCs()
       self.close()

#Details zum Ressourcenkontakt
class ScrollMessageBoxRCInfo(QMessageBox):
       def __init__(self, *args, **kwargs):
           QMessageBox.__init__(self, *args, **kwargs)
           chldn = self.children()
           scrll = QScrollArea(self)
           scrll.setWidgetResizable(True)
           grd = self.findChild(QGridLayout)
           lbl = QLabel(chldn[1].text(), self)
           lbl.setWordWrap(True)

           d = args[1]

           information = {} 
           self.iff = {}

           captions = ["TEL", "MOBIL", "EMAIL", "STR", "NUM", "PLZ", "ORT", "GEB", "IBAN", "BIC"]
           
           flo = QFormLayout()
           flo.setAlignment(Qt.AlignTop)
           
           infos = dbaccess.allCategoriesAll(d) 
            
           flo.addRow("", lbl)

           i=0                
           for inf in infos:
               e = QLineEdit(inf)
               e.setObjectName(d)
               e.setFixedHeight(22)
               e.textChanged.connect(partial(self.estateDel, captions[i], information, e))
               flo.addRow(captions[i], e)
               i+=1
           
           lbl2 = QLabel()
           lbl2.setLayout(flo)
           scrll.setWidget(lbl2)            
           scrll.setMinimumSize (400,200)      
           grd.addWidget(scrll,0,1)
           
           chldn[1].setText('')
      
           self.buttonClicked.connect(self.msgButtonClickSV)
      
           self.exec_()


       def estateDel(self, changedcol, information, e):

           information[changedcol] = e.text()
           information["NAME"] = e.objectName()
        
           self.iff = information

       def msgButtonClickSV(self):
           if len(self.iff) > 1:
               
               isError = False
               
               if "EMAIL" in self.iff:  #NICE TO HAVE: Validate IBAN und BIC verifizieren.
                   email = self.iff['EMAIL']
                   if not validators.validatemail(email):
                       self.showWarningFollowing("Ungültige Email!")
                       isError = True
               
               if "GEB" in self.iff:
                   gebtag = self.iff['GEB']
                   if not validators.validategebtag(gebtag):
                       self.showWarningFollowing("Ungültige Zeitangabe!")
                       isError = True
               
               if not isError:
                   dbaccess.updateCres2(self.iff) 

       def showWarningFollowing(self, warning):
           msg = QMessageBox()
           msg.setIcon(QMessageBox.Warning)
           msg.setText(warning)
           msg.setWindowTitle("!")
           msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
           msg.exec_()


#Hier können Ressourcenkontakte mit dem bearbeiteten Termin verknüpft werden.
class ScrollMessageBox(QMessageBox):
    def btnstate(self,b,date):
        
        name = b.objectName()
        
        if date.endswith("_"):
            date = date.split("_")[0]
        
        if b.isChecked():
           dbaccess.insertIntoCresWith(name, date[0:16]) 

        if not b.isChecked():
           dbaccess.deleteFromCresWith(name, date[0:16]) 


    def showFiltered(self, a, b, fltrtext):
        self.close()
        ScrollMessageBox(a, b, fltrtext.toPlainText())
    
    def button_releasedRC(self, nameshow):
       ScrollMessageBoxRCInfo(QMessageBox.Information, nameshow, '')

    
    def __init__(self, *args, **kwargs):
      QMessageBox.__init__(self, *args, **kwargs)
      
      scroll = QScrollArea(self)
      scroll.setWidgetResizable(True)
      self.content = QWidget()
      scroll.setWidget(self.content)
      scroll.setMinimumSize (400,200)
      lay = QVBoxLayout(self.content)
      
      d = args[1].split("_")[0]
      
      description = "" 
      
      if args[1].endswith("_"):
          description = args[1].split("_")[1]
      
      lay.addWidget(QLabel(description)) 
      
      uncheckedResContacts = dbaccess.getUncheckedResContactsFor2(d) 
      checkedResContacts = dbaccess.getCheckedResContactsFor2(d)  
      self.chckBoxes = {}
      f_text = args[2]
      for rescontact, nme in checkedResContacts.items():
          if len(f_text)<1:
              cb = QCheckBox("Check to connect " + rescontact) 
              cb.setChecked(True)
              cb.setObjectName(rescontact)
              cb.stateChanged.connect(partial(self.btnstate, cb, nme))
              resc = QPushButton(rescontact)
              resc.released.connect(partial(self.button_releasedRC, rescontact))   
              self.chckBoxes[rescontact] = True
              lay.addWidget(cb)
              lay.addWidget(resc)
          else:
              if f_text.lower() in rescontact.lower():
                  cb = QCheckBox("Check to connect " + rescontact) 
                  cb.setChecked(True)
                  cb.setObjectName(rescontact)
                  cb.stateChanged.connect(partial(self.btnstate, cb, nme))
                  resc = QPushButton(rescontact)
                  resc.released.connect(partial(self.button_releasedRC, rescontact))   
                  self.chckBoxes[rescontact] = True
                  lay.addWidget(cb)
                  lay.addWidget(resc)

      for entry in checkedResContacts:
          if entry in uncheckedResContacts:
              uncheckedResContacts.pop(entry)

      for rescontact, nme in uncheckedResContacts.items():
          if len(f_text)<1:
              cb = QCheckBox("Check to connect " + rescontact)
              cb.setChecked(False)
              cb.setObjectName(rescontact)
              cb.stateChanged.connect(partial(self.btnstate, cb, args[1]))
              resc = QPushButton(rescontact)
              resc.released.connect(partial(self.button_releasedRC, rescontact)) 
              self.chckBoxes[rescontact] = False
              lay.addWidget(cb)
              lay.addWidget(resc)
          else:
              if f_text.lower() in rescontact.lower():
                  cb = QCheckBox("Check to connect " + rescontact) 
                  cb.setChecked(False)
                  cb.setObjectName(rescontact)
                  cb.stateChanged.connect(partial(self.btnstate, cb, args[1]))
                  resc = QPushButton(rescontact)
                  resc.released.connect(partial(self.button_releasedRC, rescontact))   
                  self.chckBoxes[rescontact] = False
                  lay.addWidget(resc)
          
      filterCB = QTextEdit()
      filterCB.setStyleSheet("background-color: yellow; max-height: 2em; max-width: 22em;");
      filterCB.setPlaceholderText("Hier den Filtertext eingeben...")

      filterbtn = QPushButton("filter")
      filterbtn.resize(10, 10)
      filterbtn.setStyleSheet("background-color: yellow; height: 10px; max-width: 22em;");
      filterbtn.clicked.connect(partial(self.showFiltered, args[0], args[1], filterCB))
      
      lay.addWidget(filterCB)
      lay.addWidget(filterbtn)
      
      self.layout().addWidget(scroll, 0, 0, 1, self.layout().columnCount())
      self.exec_()


#Hier kann ein neuer Ressourcenkontakt angelegt werden.
class ScrollMessageBoxCreateRC(QMessageBox):
   fieldvalues =  ['', '', '', '', '', '', '', '', '', '', '', '', '']
   def __init__(self, *args, **kwargs):
      QMessageBox.__init__(self, *args, **kwargs)
      
      self.setWindowTitle("Neuen Ressourcenkontakt anlegen.")
      
      scroll = QScrollArea(self)
      scroll.setWidgetResizable(True)
      self.content = QWidget()
      scroll.setWidget(self.content)
      lay = QVBoxLayout(self.content)
      
      #fieldnames = ['Tel', 'Mobil', 'Email', 'Str.', 'Hausnr.', 'PLZ', 'Ort', 'Geb. Tag', 'Name', 'IBAN', 'BIC', 'neue Kategorie']
      fieldnames = ['Tel', 'Mobil', 'Email', 'Str.', 'Hausnr.', 'PLZ', 'Ort', 'Geb. Tag', 'Name', 'IBAN', 'BIC']
      categories = []
      
      for r in dbaccess.allCategories2(): 
          categories.append(r[0])
      
      for i in range(0, len(fieldnames)):
          
          te = QTextEdit('', self)
          te.setFixedHeight(22)
          
          te.setObjectName(str(i))

          if i == 7:
              te.setPlaceholderText("JJJJ-MM-TT")
          
          
          te.textChanged.connect(partial(self.testate, te, self.fieldvalues))   
          
          qlabel = QLabel(fieldnames[i],self)
          qlabel.setBuddy(te)
          
          lay.addWidget(qlabel)
          lay.addWidget(te)
          
      self.buttonClicked.connect(self.msgButtonClick)
      self.layout().addWidget(scroll, 0, 0, 1, self.layout().columnCount())
      self.setStyleSheet("QScrollArea{min-width:410 px; min-height: 600px}")
  
   def cbstate(self, cb, fieldvalues):
       fieldvalues[12] = cb.currentText()
       
   def testate(self, te, fieldvalues):
       field = te.objectName()
       fieldvalues[int(field)] = te.toPlainText()
       
   def msgButtonClick(self, i):
       if i.text().upper() == "OK":
           self.validate_save(self.fieldvalues)

    
   def showWarningFollowing(self, warning):
       msg = QMessageBox()
       msg.setIcon(QMessageBox.Warning)
       msg.setText(warning)
       msg.setWindowTitle("!")
       msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
       msg.exec_()
           
   def validate_save(self, fieldvalues):
       tel = fieldvalues[0]
       self.fieldvalues[0] = "" 
       mobil = fieldvalues[1]
       self.fieldvalues[1] = "" 
       email = fieldvalues[2]
       self.fieldvalues[2] = ""
       str = fieldvalues[3]
       self.fieldvalues[3] = "" 
       hnr = fieldvalues[4]
       self.fieldvalues[4] = "" 
       plz = fieldvalues[5]
       self.fieldvalues[5] = "" 
       ort = fieldvalues[6]
       self.fieldvalues[6] = "" 
       gebtag = fieldvalues[7]
       self.fieldvalues[7] = "" 
       name = fieldvalues[8]
       self.fieldvalues[8] = "" 
       iban = fieldvalues[9]
       self.fieldvalues[9] = "" 
       bic = fieldvalues[10]
       self.fieldvalues[10] = "" 
       cat = fieldvalues[11].upper()
       self.fieldvalues[11] = ""
       cat2 = fieldvalues[12]
       self.fieldvalues[12] = ""

       cattosave = ""
       
       if(cat2 == "Kategorie hinzufügen"):
           cattosave = cat

       else:
           cattosave = cat2

      #Der Name muss eindeutig sein, d. h. FEHLER, wenn der name schon vergeben ist in der DB.
       isnameextant = False
       for rc in dbaccess.allRC():
           if name == rc[9]:
               isnameextant = True

       isError = False        
       
       if len(name)<1:
           dlg = CustomDialog(self)
           dlg.exec()
           dlg.close()
           self.showWarningFollowing("Terminname fehlt!")
           isError = True

       if isnameextant == True or len(name)>200:
           dlg = CustomDialog(self)
           dlg.exec()
           dlg.close()
           self.showWarningFollowing("Terminname vorhanden oder zu lang!")
           isError = True

       if not validators.validatemail(email):  #NICE TO HAVE: Validate IBAN und BIC verifizieren.
           dlg = CustomDialog(self)
           dlg.close()
           self.showWarningFollowing("Ungültige Email!")
           isError = True

       if not validators.validategebtag(gebtag):
           dlg = CustomDialog(self)
           dlg.exec()
           dlg.close()
           self.showWarningFollowing("Ungültige Zeitangabe!")
           isError = True
       
       if not isError:    
           if len(cattosave) > 0:
               name = cattosave.upper() + "_" + name    
           
           dbaccess.insertNewRC2(tel, mobil,  email,  str, hnr,  plz,  ort,  gebtag,  name,  iban,  bic,  cattosave) 
       
#Bisher implementierte Fehler erhalten Meldungen.
class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Info")
        QBtn = QDialogButtonBox.Ok 
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.layout = QVBoxLayout()
        message = QLabel("Fehler bei der Eingabe!")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

#######################################################################################################################################

#Hauptklasse
class MainWindow(QMainWindow):
    
    singleton: 'MainWindow' = None
    
    def __init__(self, filtervals):
        super().__init__()

        self.printAppointments()
       
        tb = QToolBar(self)
        
        cal = QCalendarWidget(self) 
        cal.setGridVisible(True)

        monthly = QPushButton("T. monatlich") 
        weekly = QPushButton("T. wöchentlich")
        
        cb = QComboBox()
        cb.addItem("Monatsansicht")
        cb.addItem("Wochenansicht")
        cb.addItem("Tagesansicht")
        cb.addItem("Jahresansicht")
        
        cal.clicked[QtCore.QDate].connect(partial(self.cal_clicked_filter, cal, cb)) 

        widget = QWidget()         
        vlayout = QVBoxLayout()
        vlayout.addWidget(cb)
        
        monthly.setObjectName('monthly') 
        weekly.setObjectName('weekly')
        
        monthly.released.connect(partial(self.button_releasedMonthlyOrWeekly))
        weekly.released.connect(partial(self.button_releasedMonthlyOrWeekly))
        
        vlayout.addWidget(monthly)
        vlayout.addWidget(weekly)
        
        datechooser = QPushButton("Einzeltermin anlegen")
        datechooser.setObjectName('datechooser')
        datechooser.released.connect(partial(self.create_date))
        vlayout.addWidget(datechooser)
        
        pathchooser = QPushButton("Pfad wählen")
        pathchooser.setObjectName('pathchooser')
        pathchooser.released.connect(partial(self.choosePath))
        vlayout.addWidget(pathchooser)
        
        seriesdel = QPushButton("Terminserie löschen")
        seriesdel.setObjectName('seriesdel')
        seriesdel.released.connect(partial(self.deleteSeries))
        vlayout.addWidget(seriesdel)
        
        widget.setLayout(vlayout)

        tb.addWidget(cal)
        tb.addWidget(widget)       
        tb.setAllowedAreas(Qt.TopToolBarArea)
        tb.setFloatable(False)
        tb.setMovable(False)
        
        self.addToolBar(tb)

        appointmentDict = dbaccess.allAppointments()
      
        grid_layout = QGridLayout()
        self.widget = QWidget()
        self.widget.setLayout(grid_layout)
        self.scroll = QScrollArea()  

        aktuellesDatum = datetime.date.today()
        kw = aktuellesDatum.isocalendar()[1] 
        
        button = QPushButton(" Kalenderwoche-(" + str(kw) + ")---------------- Datum des Termins mit Wochentag - Termin (zum Bearbeiten klicken)")
        button.setStyleSheet("text-align: left;font-weight: bold; font-size: 14px; color:black")
        button.setEnabled(False)
        
        grid_layout.setAlignment(Qt.AlignTop)
        
        grid_layout.addWidget(button, 0, 0, 1, 3)
        
        create = QPushButton("ResKontakt neu")
        create.resize(10, 10)
        create.clicked.connect(self.showdialogRD)
        
        grid_layout.addWidget(create, 0, 3, 1, 3)

        
        filteredDict = {}
        
        if filtervals[0] == "" and filtervals[1] == "" and filtervals[2] == "":
            filteredDict = appointmentDict
            
        else: 
            filteredDict = self.filter(appointmentDict, filtervals)
        
        keys = []
        
        for k in filteredDict.keys():
            keys.append(k)
        
        values = []
        
        for v in filteredDict.values():
            values.append(v)
        
        enddates = dbaccess.allEnddates()
        
        i=0        
        for x in range(1, len(filteredDict)+1):
            for y in range(0, 5):
                button = QPushButton(values[i])
                button.setObjectName('Appointment%d' % x)
                button.released.connect(partial(self.showdialogAppointment,filteredDict)) 
                date = QPushButton(keys[i])
                date.setStyleSheet("color:black")
                date.setEnabled(False)
                delete = QPushButton("del")
                delete.resize(10, 10)
                delete.setObjectName('Button%d' % x)
                delete.released.connect(partial(self.button_released, filteredDict)) 
               
                ansicht = QPushButton("Beschreibung")
                ansicht.resize(10, 10)
                ansicht.setObjectName('Ansicht%d' % x)
                ansicht.released.connect(partial(self.button_releasedDescription, filteredDict))
                
                if y == 0:
                    dt = date.text().split(" ")[0].split("-")
                    kw = datetime.date(year=int(dt[0]), month=int(dt[1]), day=int(dt[2])).isocalendar()[1] 
                    date.setText("KW: " + str(kw))
                    grid_layout.addWidget(date, x, y)
                if y == 1:
                    dt = date.text().split(" ")[0].split("-")
                    enddt = enddates[date.text()]
                    intDay = datetime.date(year=int(dt[0]), month=int(dt[1]), day=int(dt[2])).weekday()
                    days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
                    date.setText(date.text() + "-" + enddt.split(" ")[1] + ", " +  days[intDay]) 
                    grid_layout.addWidget(date, x, y)
                if y == 2:
                    grid_layout.addWidget(button, x, y)
                if y == 3:
                    grid_layout.addWidget(delete, x, y)
                if y == 4:
                    grid_layout.addWidget(ansicht, x, y) 
            
            i+=1
        
        tdrucken = QPushButton("Drucke Termine")
        tdrucken.released.connect(self.printAppointments) 
        grid_layout.addWidget(tdrucken, len(filteredDict)+1, 0)                        
        resdrucken = QPushButton("Drucke Reskontakte")
        resdrucken.released.connect(partial(self.printRescontacts))
        grid_layout.addWidget(resdrucken, len(filteredDict)+2, 0)
        resdelete = QPushButton("Reskontakt(e) anzeigen / zum Löschen markieren")
        resdelete.released.connect(partial(self.showRescontacts))
        grid_layout.addWidget(resdelete, len(filteredDict)+3, 0)       
        
        read_contacts = QPushButton("Lese Termine ein")
        read_contacts.released.connect(partial(self.readAllAppointments))
        grid_layout.addWidget(read_contacts, len(filteredDict)+4, 0)       
        
        read_contacts = QPushButton("Lese Kontakte ein")
        read_contacts.released.connect(partial(self.readAllContacts))
        grid_layout.addWidget(read_contacts, len(filteredDict)+5, 0)       

         
        allappointmentsdelete = QPushButton("Alle Termine löschen")
        allappointmentsdelete.released.connect(partial(self.deleteAllAppointments))
        grid_layout.addWidget(allappointmentsdelete, len(filteredDict)+6, 0)        
                
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)
        self.setWindowTitle("pycrm5")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: lightgreen;')
        self.setGeometry(90, 90, 950, 600)
        self.show()

        return


    def readAllAppointments(self):
        Tk().withdraw()
        filename = askopenfilename()
        if len(filename) > 0:
            filereader.readContactFile(filename, 4)
            self.close()
            self.restart(["", "", ""])

    def readAllContacts(self):
        Tk().withdraw()
        filename = askopenfilename()
        if len(filename) > 0:
            filereader.readContactFile(filename, 12)

    def showWarningFollowing(self, warning):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(warning)
        msg.setWindowTitle("!")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()

    def defaultDir(self):
        arr = os.getcwd().split("\\")[:-2]
        s = ""
        for file in arr:
            s+=file
            s += "\\"
        return s

    def getDirPath(self):
        path = dbaccess.selectFromSettings()
        
        p = ""
        
        if len(path[0][0]) > 0:
            
            try:
                p = path[0][0].replace("/", "\\\\")
            
            except:
               dbaccess.insertIntoSettingsPath("") 
               self.close()
               self.restart(["", "", ""])
            
            p+="\\\\"
        
        else:
            self.showWarningFollowing("Bitte erst Verzeichnis wählen, wohin gedruckt werden soll!")
        
        return p


    def printRescontacts(self):
        rcs = dbaccess.allRC()
        
        directory = self.getDirPath()
        
        if len(directory) > 0:
            with open(directory+"rescontcts.csv", "w", encoding="utf8") as f:
            
                for x in rcs:
                    r = str(x)[1:-1]
                    
                    f.write(r.split(",")[0].strip() + ", " + r.split(",")[1].strip() + ", " + r.split(",")[2].strip() + ", " + r.split(",")[3].strip() + ", " + r.split(",")[4].strip() + ", " + r.split(",")[5].strip() + ", " + r.split(",")[6].strip() + ", " + r.split(",")[7].strip() + ", " + r.split(",")[9].strip() + ", " + r.split(",")[10].strip() + ", " + r.split(",")[11].strip() + "\n")
        
            f.close()

    def deleteAllAppointments(self):
        msg_save_all = QMessageBox()
        msg_save_all.setIcon(QMessageBox.Question)
        msg_save_all.setWindowTitle("Alle löschen?")
        msg_save_all.setText("Wollen Sie alle Termine löschen?")
        msg_save_all.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        ret = msg_save_all.exec();
        
        delete = False
        
        if ret == QMessageBox.Ok:
            delete = True

        if ret == QMessageBox.Cancel:
            delete = False


        if delete:
            dbaccess.deleteFromAppointmentsAndCRes()
        
        self.close()
        self.restart(["", "", ""])



    def showRescontacts(self):
        result = ScrollMessageBoxShowResourceContacts(None)
        result.exec_()


    def printAppointments(self):
        appointmentDict = dbaccess.allAppointments() 
        
        appointmentEnddatesDict = dbaccess.allEnddates()
        
        directory = self.getDirPath()
        
        if len(directory) > 0:
            with open(directory+"termine.csv", "w", encoding="utf8") as f:
                for datum, title in appointmentDict.items():
                    desc = dbaccess.selectDescriptionFor2(datum)[0][0]    
                    f.write(datum + ", " + title + ", " + desc + ", " + appointmentEnddatesDict[datum] + "\n")
        
            f.close()


    def withinWeek(self, chosen, key):
        test_list = [key]
        cy = int(chosen.split("-")[0])
        cm = int(chosen.split("-")[1])
        cd = int(chosen.split("-")[2])

        wochentag = datetime.datetime(cy, cm, cd).strftime('%A')
        subtrahieren = {"Monday" : 0, "Tuesday" : 1, "Wednesday" : 2, "Thursday" : 3, "Friday" : 4, "Saturday" : 5, "Sunday" : 6} 
        addieren = {"Monday" : 6, "Tuesday" : 5, "Wednesday" : 4, "Thursday" : 3, "Friday" : 2, "Saturday" : 1, "Sunday" : 0}
        
        ini_time_for_now = datetime.datetime(cy, cm, cd)

        future_date_after_ndays = ini_time_for_now + \
                         timedelta(days = int(addieren[wochentag]))
        
        
        past_date_before_ndays = ini_time_for_now - \
                         timedelta(days = int(subtrahieren[wochentag]))
 
        date_strt, date_end = past_date_before_ndays, future_date_after_ndays
        
        res = False

        for key in test_list:
            key = key[0:10]
            if datetime.datetime(int(key.split("-")[0]), int(key.split("-")[1]), int(key.split("-")[2])) >= date_strt and datetime.datetime(int(key.split("-")[0]), int(key.split("-")[1]), int(key.split("-")[2])) <= date_end:
                res = True
  

        return res 


    def filter(self, dict, filtervals):
        returndict = {}
        #Tag:
        if filtervals[0] != "" and filtervals[1] != "" and filtervals[2] != "":
            if "w" in filtervals[2]:
                chosen = filtervals[0] + "-" + filtervals[1] + "-" + filtervals[2][:-1]
                for key in dict:
                    if self.withinWeek(chosen, key):
                        returndict[key]=dict[key]
            else:     
                for key in dict:
                    if(key.split(" ")[0] == filtervals[0] + "-" + filtervals[1] + "-" + filtervals[2]):
                        returndict[key]=dict[key]
        
        #Monat:
        if filtervals[0] == "" and filtervals[1] != "" and filtervals[2] != "":
            for key in dict:
                if(key.split(" ")[0].split("-")[1] == filtervals[1] and key.split(" ")[0].split("-")[0] == filtervals[2]):
                    returndict[key]=dict[key]
        
        #Jahr
        if filtervals[0] != "" and filtervals[1] == "" and filtervals[2] == "":
            for key in dict:
                if(key.split(" ")[0].split("-")[0] == filtervals[0]):
                    returndict[key]=dict[key]
        
        return returndict

    def button_releasedDescription(self, filteredDict):
        sending_button = self.sender()

        index = sending_button.objectName()[7:] 
        
        date = "0000-00-00 00:00"
        nname = ""
        desc = ""
        
        i = 1
        for k, v in filteredDict.items():
            if int(i) == int(index):
                desc = dbaccess.selectDescriptionFor2(k)[0][0] 
                date = k
            i+=1
        
        title = ""
        
        if len(desc) > 0:
            title = date + "_" + desc
        
        else:
            title = date
        
        ScrollMessageBox(QMessageBox.Information, title, "")
        
        self.close()
        self.restart(["", "", ""])

    def button_released(self, filteredDict):
        sending_button = self.sender()
        
        index = sending_button.objectName()[6:]
        
        i = 1
        for k in filteredDict:
            if int(i) == int(index):
                dbaccess.deleteAppointment2(k) 
            i+=1
        
        self.close()
        self.restart(["", "", ""])
        
    def showdialogAppointment(self, filteredDict):
        sending_button = self.sender()

        btn = sending_button.objectName()[11:]
        
        termin_alt = ""
        
        i = 1
        for k in filteredDict:
            if int(i) == int(btn): 
                uhrzeit_anfang = k[11:13]
                uhrzeit_ende = k[14:16]
                termin = k.split(" ")[0]
                tbeschreibung = dbaccess.selectDescriptionFor2(k)[0][0]   
                ttitel = dbaccess.selectNameFor2(k)[0][0]
                
                termin_alt = k
                 
            i+=1
      
        dlg = QDialog()
        dlg.resize(400, 300)
            
        title = QLabel("Termintitel", dlg)
        title.move(20, 20)
            
        termintitel = QLineEdit(dlg)
        termintitel.setText(ttitel)
        termintitel.move(50,50)
        termintitel.resize(260, 20)
            
        description = QLabel("Terminbeschreibung", dlg)
        description.move(20, 80)
            
        terminbeschreibung = QLineEdit(dlg)
        terminbeschreibung.setText(tbeschreibung) 
        terminbeschreibung.move(50,100)
        terminbeschreibung.resize(260, 20)
            
        hour = QLabel("Beginn Std.", dlg)
        hour.move(20, 136)
            
        uhrzeit = QComboBox(dlg)

        uhrzeit.addItems(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"])
        
        std = uhrzeit_anfang.split(":")[0]
        i = 0
        for i in range (0, uhrzeit.count()):
            if std == self.formatDayMonth(str(i)):
                uhrzeit.setCurrentIndex(i)
            
        uhrzeit.move(50, 151)

        minute = QLabel("Beginn Min.", dlg)
        minute.move(100, 136)
            
        minuten = QComboBox(dlg)
        minuten.addItems(["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "59"])
 

        hour_end = QLabel("Ende Std.", dlg)
        hour_end.move(190, 136)
            
        uhrzeit_end = QComboBox(dlg)
        uhrzeit_end.addItems(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"])
        uhrzeit_end.move(220, 151)


        minute_end = QLabel("Min.", dlg)
        minute_end.move(270, 136)
            
        minuten_end = QComboBox(dlg)
        minuten_end.addItems(["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "59"])
        minuten_end.move(270, 151)

 
        min = uhrzeit_ende
        i = 0
        for i in range (0, minuten.count()):
            if min == self.formatDayMonth(str(i)):
                minuten.setCurrentIndex(i)

        minuten.move(100, 151)

        date = QLabel("Datum", dlg)        
        date.move(20, 180)
            
        datum = QLineEdit(dlg)
        datum.setMaxLength(10)
        datum.setText(termin)
        datum.move(20,200)
        datum.resize(260, 20)

        ok = QPushButton("OK", dlg)
        ok.move(50, 230)
    
        ok.released.connect(partial(self.button_releasedUniqueEdit, termintitel, terminbeschreibung, uhrzeit, minuten, datum, btn, dlg, termin_alt, uhrzeit_end, minuten_end))
    
        dlg.setWindowTitle("Termin") 
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()  

            
    def showdialogRD(self): 
        result = ScrollMessageBoxCreateRC(None)
        result.exec_()
          
        
    def monthlies(self, year, month, day, uhrzeit):
        datesMonthly = []
        dateinput = year + "-" + month +"-" + day+" " + uhrzeit
        datesMonthly.append(dateinput) 
        y = int(year)
        y+=1
        while int(str(dateinput)[0:4]) < y:
            new_date = datetime.datetime.strptime(year + "-" + month +"-" + day,"%Y-%m-%d")
            aMonth = datetime.timedelta(weeks = 4)
            dateinput = new_date + aMonth
            dateinput = str(dateinput)[0:10]
            year = dateinput[0:4]
            month = dateinput[5:7]
            day = dateinput[8:10]
            datesMonthly.append(year + "-" + month + "-" + day + " " + uhrzeit)
        datesMonthly.pop(-1)
        return datesMonthly    
        
    def weeklies(self, year, month, day, uhrzeit):
        datesWeekly = []
        dateinput = year + "-" + month +"-" + day+" " + uhrzeit 
        datesWeekly.append(dateinput)
        y = int(year)
        y+=1
        while int(str(dateinput)[0:4]) < y:
            new_date = datetime.datetime.strptime(year + "-" + month +"-" + day,"%Y-%m-%d")
            aWeek = datetime.timedelta(weeks = 1)
            dateinput = new_date + aWeek
            dateinput = str(dateinput)[0:10]
            year = dateinput[0:4]
            month = dateinput[5:7]
            day = dateinput[8:10]
            datesWeekly.append(year + "-" + month + "-" + day + " " + uhrzeit)
        datesWeekly.pop(-1)   
        return datesWeekly       
          
    def cal_clicked_filter(self, cal, cb):
        filtervals = ['', '', '']
        date = str(cal.selectedDate())
        lt = date.rindex('(')
        gt = date.rindex(')')
        ansicht = cb.currentText()
        if ansicht == "Tagesansicht":
            filtervals[0] = date[lt+1:gt].split(', ')[0]
            filtervals[1] = self.formatDayMonth(date[lt+1:gt].split(', ')[1])
            filtervals[2] = self.formatDayMonth(date[lt+1:gt].split(', ')[2])
            
        if ansicht == "Monatsansicht":
            filtervals[1] = self.formatDayMonth(date[lt+1:gt].split(', ')[1])
            filtervals[2] = self.formatDayMonth(date[lt+1:gt].split(', ')[0])
            
        if ansicht == "Wochenansicht":
            filtervals[0] = date[lt+1:gt].split(', ')[0]
            filtervals[1] = self.formatDayMonth(date[lt+1:gt].split(', ')[1])
            filtervals[2] = self.formatDayMonth(date[lt+1:gt].split(', ')[2]) + "w"    
            
        if ansicht == "Jahresansicht":
            filtervals[0] = date[lt+1:gt].split(', ')[0]    

 
        self.close()
        self.restart(filtervals)
    
    def create_date(self):
        
        sending_button = self.sender()
        btn = sending_button.objectName()
         
        dlg = QDialog()
        dlg.resize(400, 300)
            
        title = QLabel("Termintitel", dlg)
        title.move(20, 20)
            
        termintitel = QLineEdit(dlg)
        termintitel.move(50,50)
        termintitel.resize(260, 20)
            
        description = QLabel("Terminbeschreibung", dlg)
        description.move(20, 80)
            
        terminbeschreibung = QLineEdit(dlg)
        terminbeschreibung.move(50,100)
        terminbeschreibung.resize(260, 20)
            
        hour = QLabel("Beginn Std.", dlg)
        hour.move(20, 136)
            
        uhrzeit = QComboBox(dlg)
        uhrzeit.addItems(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"])
        uhrzeit.move(50, 151)


        minute = QLabel("Min.", dlg)
        minute.move(100, 136)
            
        minuten = QComboBox(dlg)
        minuten.addItems(["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "59"])
        minuten.move(100, 151)


        hour_end = QLabel("Ende Std.", dlg)
        hour_end.move(190, 136)
            
        uhrzeit_end = QComboBox(dlg)
        uhrzeit_end.addItems(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"])
        uhrzeit_end.move(220, 151)


        minute_end = QLabel("Min.", dlg)
        minute_end.move(270, 136)
            
        minuten_end = QComboBox(dlg)
        minuten_end.addItems(["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "59"])
        minuten_end.move(270, 151)


        date = QLabel("Datum", dlg)
        date.move(20, 180)
            
        datum = QLineEdit(dlg)
        datum.setMaxLength(10)
        datum.setPlaceholderText("JJJJ-MM-TT")
        datum.move(20,200)
        datum.resize(260, 20)

        ok = QPushButton("OK", dlg)
        ok.move(50, 230)
    
        ok.released.connect(partial(self.button_releasedUnique, termintitel, terminbeschreibung, uhrzeit, minuten, datum, btn, dlg, uhrzeit_end, minuten_end))
    
        dlg.setWindowTitle(btn) 
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()
    
    
    def deleteSeries(self):
        dlg = QDialog()
        dlg.resize(200, 170)
            
        datum = QLineEdit(dlg)
        datum.setPlaceholderText("JJJJ-MM-TT")
        datum.setMaxLength(10)
        datum.move(20,20)
        
        uhrzt = QLineEdit(dlg)
        uhrzt.setPlaceholderText("HH:MM")
        uhrzt.setMaxLength(5)
        uhrzt.move(20,40)

        
        okW = QPushButton("wöchentlich löschen", dlg) 
        okW.move(20, 70)
        okW.released.connect(partial(self.button_releasedDelSeries, "w", datum, uhrzt, dlg))

        okM = QPushButton("monatlich löschen", dlg) 
        okM.move(20, 98)
        okM.released.connect(partial(self.button_releasedDelSeries, "m", datum, uhrzt, dlg))
        
        
        dlg.setWindowTitle("Serie löschen!") 
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()
    
    
    
    def button_releasedDelSeries(self, mw, date, u, dlg):
        dtum = date.text()
        uhzt = u.text()
        
        isValidDate = validators.validatedatum(dtum)
        isValidTime = validators.validatetime(uhzt)
        
        isError = False
        
        if not (isValidDate and isValidTime):
            dlg = CustomDialog(self)
            dlg.close()
            self.showWarningFollowing("Ungültige Zeiteingabe!")
            isError = True

        if not isError:
         
         year = dtum[0:4]
         month = dtum[5:7]
         day = dtum[8:10]

         uhrzeit = uhzt 
         
         if mw == "m":
             monthlies = self.monthlies(year, month, day, uhrzeit)
             dbaccess.deleteSeries(monthlies)    
    
 
        if mw == "w":   
            wklies = self.weeklies(year, month, day, uhrzeit)
            dbaccess.deleteSeries(wklies)
    
        dlg.close()
    
        self.close()
        self.restart(["", "", ""])
            
    
    def choosePath(self):
        root = Tk()
        root.withdraw()
        root.update()
        pathString = askdirectory()
        dbaccess.insertIntoSettings(pathString)
        root.destroy()
    
    def button_releasedMonthlyOrWeekly(self): 
        sending_button = self.sender()
        btn = sending_button.objectName()
         
        dlg = QDialog()
        dlg.resize(400, 300)
            
        title = QLabel("Termintitel", dlg)
        title.move(20, 20)
            
        termintitel = QLineEdit(dlg)
        termintitel.move(50,50)
        termintitel.resize(260, 20)
            
        description = QLabel("Terminbeschreibung", dlg)
        description.move(20, 80)
            
        terminbeschreibung = QLineEdit(dlg)
        terminbeschreibung.move(50,100)
        terminbeschreibung.resize(260, 20)
            
        hour = QLabel("Beginn Std.", dlg)
        hour.move(20, 136)
            
        uhrzeit = QComboBox(dlg)
        uhrzeit.addItems(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"])
        uhrzeit.move(50, 151)


        minute = QLabel("Min.", dlg)
        minute.move(100, 136)
            
        minuten = QComboBox(dlg)
        minuten.addItems(["00", "05", "10", "15", "25", "30", "35", "40", "45", "50", "55", "59"])
        minuten.move(100, 151)

        hour_end = QLabel("Ende Std.", dlg)
        hour_end.move(190, 136)
            
        uhrzeit_end = QComboBox(dlg)
        uhrzeit_end.addItems(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"])
        uhrzeit_end.move(220, 151)

        minute_end = QLabel("Min.", dlg)
        minute_end.move(270, 136)
            
        minuten_end = QComboBox(dlg)
        minuten_end.addItems(["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "59"])
        minuten_end.move(270, 151)

        date = QLabel("Datum", dlg)
        date.move(20, 180)
            
        datum = QLineEdit(dlg)
        datum.setPlaceholderText("JJJJ-MM-TT")
        datum.setMaxLength(10)
        datum.move(20,200)
        datum.resize(260, 20)

        ok = QPushButton("OK", dlg) 
        ok.move(50, 230)
        ok.released.connect(partial(self.button_releasedSeries, termintitel, terminbeschreibung, uhrzeit, minuten, datum, btn, dlg, uhrzeit_end, minuten_end)) 
            
        add_these_rcs = QPushButton("Ressourcenk. hinzufügen", dlg)
        add_these_rcs.move(130, 230)
        add_these_rcs.released.connect(partial(self.rc_add))
           
        dlg.setWindowTitle(btn) 
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()
   
   
    def rc_add(self):
        result = ScrollMessageBoxShowResourceContactsAdd(None)
        result.exec_() 

    def button_releasedUnique(self, termintitel, terminbeschreibung, sts, min, datum, btn, dlg, uhrzeit_end, minuten_end):
        date = datum.text()
        
        ttitel = termintitel.text()
        if len(ttitel) < 1:
            ttitel = "Neuer Termin!"
        tbeschreibung = terminbeschreibung.text()
        
        hh = sts.currentText()
        mm = min.currentText()
    
        isError = False     
        
        hh_end = uhrzeit_end.currentText()
        mm_end = minuten_end.currentText()
        
        start_zeit = datetime.datetime.strptime(hh+":"+mm, "%H:%M")
        end_zeit = datetime.datetime.strptime(hh_end+":"+mm_end, "%H:%M")
        isError = start_zeit > end_zeit
        
        
        uhrzeit = self.formatDayMonth(str(hh)) + ":" + self.formatDayMonth(str(mm))
        
        uhrzeit_end = self.formatDayMonth(str(hh_end)) + ":" + self.formatDayMonth(str(mm_end))
                
        isValidDate = validators.validatedatum(date)
    
        if not isValidDate:
            dlg = CustomDialog(self)
            dlg.close()
            self.showWarningFollowing("Ungültige Zeiteingabe!")
            isError = True

        if not isError:
            
            year = date.split("-")[0]
            month = date.split("-")[1] 
            day = date.split("-")[2]

            dateinput = year + "-" + month +"-" + day+ " " + uhrzeit
            dateinput_end = year + "-" + month +"-" + day+ " " + uhrzeit_end
            
            isError = False

            dict = dbaccess.allAppointments()             
            enddates = dbaccess.allEnddates()
            
            for dts in dict.keys():
                end = enddates[dts]
                if validators.isDateBetween(dts, dateinput, end) or validators.isDateBetween(dts, dateinput_end, end): 
                    self.showWarningFollowing("Überschneidung!")
                    isError = True
              
            #Dieser Termin ist als Dummytermin für neu angelegte Kontaktressourcen vorbehalten. 
            if dateinput == "0000-00-00 00:00":
                self.showWarningFollowing("Ungültige Zeiteingabe!")
                isError = True
    
            if not isError:             
                dbaccess.insertAppointment(dateinput, ttitel, tbeschreibung, dateinput_end)
         
            dlg.close()
    
            self.close()
            self.restart(["", "", ""])

   
    def button_releasedUniqueEdit(self, termintitel, terminbeschreibung, sts, min, datum, btn, dlg, termin_alt, uhrzeit_end, minuten_end):
        date = datum.text()
        
        ttitel = termintitel.text()
        if len(ttitel) < 1:
            ttitel = "Neuer Termin!"
        tbeschreibung = terminbeschreibung.text()
        
        hh = sts.currentText()
        mm = min.currentText()
        
        uhrzeit = self.formatDayMonth(str(hh)) + ":" + self.formatDayMonth(str(mm))
                
        isValidDate = validators.validatedatum(date)
    
        isError = False
    
        hh_end = uhrzeit_end.currentText()
        mm_end = minuten_end.currentText()
        
        start_zeit = datetime.datetime.strptime(hh+":"+mm, "%H:%M")
        end_zeit = datetime.datetime.strptime(hh_end+":"+mm_end, "%H:%M")
        isError = start_zeit > end_zeit
        
        if isError:
            self.showWarningFollowing("Ungültige Zeiteingabe!")
            
    
        if not isValidDate:
            dlg = CustomDialog(self)
            dlg.close()
            self.showWarningFollowing("Ungültige Zeiteingabe!")
            isError = True

        if not isError:
            
            year = date.split("-")[0]
            month = date.split("-")[1] 
            day = date.split("-")[2]

            dateinput = year + "-" + month +"-" + day+ " " + uhrzeit
            dateinput_end = year + "-" + month +"-" + day+ " " + hh_end + ":" + mm_end

            dict = dbaccess.allAppointments()
            enddates = dbaccess.allEnddates()
            
            isErrorOrBlock = False

            #Dieser Termin ist als Dummytermin für neu angelegte Kontaktressourcen vorbehalten. 
            if dateinput == "0000-00-00 00:00":
                self.showWarningFollowing("Ungültige Zeiteingabe!")
                isErrorOrBlock = True
            
            enddates = dbaccess.allEnddates()
            
            for dts in dict.keys():
                end = enddates[dts]
                if not termin_alt == dts:
                    if validators.isDateBetween(dts, dateinput, end) or validators.isDateBetween(dts, dateinput_end, end):  
                        self.showWarningFollowing("Überschneidung!")
                        isErrorOrBlock = True         
                        
    
            if not isErrorOrBlock:
                dbaccess.editAppointmentDateUpdate2(ttitel, tbeschreibung, termin_alt, dateinput_end)
                
                newdate = date + " " + uhrzeit
                dbaccess.editAppointment(ttitel, tbeschreibung, termin_alt, newdate)
         
            dlg.close()
    
            self.close()
            self.restart(["", "", ""])
   
   
    def button_releasedSeries(self, termintitel, terminbeschreibung, sts, min, datum, btn, dlg, uhrzeit_end, minuten_end):
        
        date = datum.text() 
        
        ttitel = termintitel.text()
        if len(ttitel) < 1:
            ttitel = "Neuer Termin!"
        tbeschreibung = terminbeschreibung.text()
        
        hh = sts.currentText()
        mm = min.currentText()
        
        isError = False
        
        hh_end = uhrzeit_end.currentText()
        mm_end = minuten_end.currentText()
        
        start_zeit = datetime.datetime.strptime(hh+":"+mm, "%H:%M")
        end_zeit = datetime.datetime.strptime(hh_end+":"+mm_end, "%H:%M")
        
        isError = start_zeit > end_zeit
        
        uhrzeit = self.formatDayMonth(str(hh)) + ":" + self.formatDayMonth(str(mm))
        uhrzeit_end = self.formatDayMonth(str(hh_end)) + ":" + self.formatDayMonth(str(mm_end))
                
        isValidDate = validators.validatedatum(date)
    
        if not isValidDate:
            dlg = CustomDialog(self)
            dlg.close()
            self.showWarningFollowing("Ungültige Zeiteingabe!")
            isError = True

        if not isError:
            
            year = date.split("-")[0]
            month = date.split("-")[1] 
            day = date.split("-")[2]

            enddates = dbaccess.allEnddates()    
            
            thedates = []
            
            if btn == "monthly":            
                monthlies = self.monthlies(year, month, day, uhrzeit)
                for m in monthlies:
                    m_with_end = m.split(" ")[0] + " " + uhrzeit_end
                    dict = dbaccess.allAppointments()
                    for dts in dict.keys():
                        end = ""
                        if dts in enddates:
                            end = enddates[dts]
                        if validators.isDateBetween(dts, m, end) or validators.isDateBetween(dts, m_with_end, end): 
                            self.showdialog()
                            isError = True

                    if not isError:
                        thedates = monthlies
                        dbaccess.insertAppointmentWithTitleAndDescription2(monthlies,ttitel, tbeschreibung, uhrzeit_end) 
         
            if btn == "weekly":
                wklies = self.weeklies(year, month, day, uhrzeit)
                for w in wklies:
                    w_with_end = w.split(" ")[0] + " " + uhrzeit_end
                    dict = dbaccess.allAppointments()
                    for dts in dict.keys():
                        end = ""
                        if dts in enddates:
                            end = enddates[dts]
                        if validators.isDateBetween(dts, w, end) or validators.isDateBetween(dts, w_with_end, end): 
                            self.showdialog()
                            isError = True

                    if not isError:
                        thedates = monthlies
                        dbaccess.insertAppointmentWithTitleAndDescription2(wklies,ttitel, tbeschreibung, uhrzeit_end)
         
            dlg.close()
    
            dbaccess.connectResourceContacts(thedates)
    
            self.close()
            self.restart(["", "", ""])

    
    def formatDayMonth(self, val):
        result = val
        
        if len(val) < 2:
            result = val.rjust(1 + len(val), '0')
            
        return result
    
    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Überschneidung!")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()

        
    @staticmethod
    def restart(filtervals):
        MainWindow.singleton = MainWindow(filtervals)


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow.restart(["", "", ""])
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


    