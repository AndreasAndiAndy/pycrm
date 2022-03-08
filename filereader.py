################################

#Author: Andreas Gölz

#This document is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License, version 3, 
#as published by the Free Software Foundation. 

################################

from PyQt5.QtWidgets import *
import dbaccess

def showWarningFollowing(warning):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(warning)
        msg.setWindowTitle("!")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()

def readContactFile(filename, breadth):
    isError = False
    
    if not filename.endswith("csv"):
        isError = True
 
 
    f = open(filename,"r")
    lines = f.readlines()

    for line in lines:
        if len(line.split(",")) != breadth:
            isError = True
      
    legendaResCon = []  
    if not isError:
        
        ######################################################################
        
        if breadth == 4:
            
            legendaAppointment = []
            
            appointmentDict = dbaccess.allAppointments2()
            if len(appointmentDict) > 0:
                for r in lines:
                    if not r.split(",")[0].strip() in appointmentDict.keys():
                        legendaAppointment.append(line)
           
            else:
                for r in lines:
                    legendaAppointment.append(r)
                    print(legendaAppointment)

            dbaccess.readListFromFile(legendaAppointment, "appointments")
        
        ######################################################################
        
        if breadth == 12:
            rescontactsThere = dbaccess.allRC2()
            if len(rescontactsThere) > 0:
                names = []
                for res in rescontactsThere:
                    names.append(res[9])
                    
                for line in lines:
                    if (line.split(",")[9].strip()[1:-1] in names == False):
                        legendaResCon.append(line.split(",")[0].strip()[1:-1] + ", " + line.split(",")[1].strip()[1:-1] + ", " + line.split(",")[2].strip()[1:-1] + ", " + line.split(",")[3].strip()[1:-1] + ", " + line.split(",")[4].strip()[1:-1] + ", " + line.split(",")[5].strip()[1:-1] + ", " + line.split(",")[6].strip()[1:-1] + ", " + line.split(",")[7].strip()[1:-1] + ", " + line.split(",")[9].strip()[1:-1] + ", " + line.split(",")[10].strip()[1:-1] + ", " + line.split(",")[11].strip()[1:-1])
            else:
                for r in lines:
                    legendaResCon.append(r.split(",")[0].strip()[1:-1] + ", " + r.split(",")[1].strip()[1:-1] + ", " + r.split(",")[2].strip()[1:-1] + ", " + r.split(",")[3].strip()[1:-1] + ", " + r.split(",")[4].strip()[1:-1] + ", " + r.split(",")[5].strip()[1:-1] + ", " + r.split(",")[6].strip()[1:-1] + ", " + r.split(",")[7].strip()[1:-1] + ", " + r.split(",")[9].strip()[1:-1] + ", " + r.split(",")[10].strip()[1:-1] + ", " + r.split(",")[11].strip()[1:-1])

            dbaccess.readListFromFile(legendaResCon, "rescon")

    else:
        showWarningFollowing("Fehler beim Einlesen!")

            
    f.close()

            