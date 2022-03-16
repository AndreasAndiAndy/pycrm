################################

#Author: Andreas Gölz

#This document is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License, version 3, 
#as published by the Free Software Foundation. 

################################


import sqlite3

conn = sqlite3.connect('pcrm.db')

cur = conn.cursor()


cur.execute(
        '''DELETE FROM auxiliaries'''
         )

cur.execute(
        '''DELETE FROM appointment'''
         )

cur.execute(
        '''DELETE FROM categories'''
         )


cur.execute(
        '''DELETE FROM cres'''
         )


cur.execute(
        '''DELETE FROM addenda'''
         )


cur.execute(
        '''DELETE FROM settings'''
         )


#conn.execute(
#        '''CREATE TABLE LOCALE
#         (
#		  LOCALE CHAR(50)
#         );'''
#         )


#conn.execute(
#        '''CREATE TABLE CRES
#         (
#		  TEL CHAR(200),
#          MOBIL CHAR(200),
#          EMAIL CHAR(200),
#          STREET CHAR(200),
#          NUM CHAR(200),
#          PLZ CHAR(200),
#          ORT CHAR(200),
#          BIRTHDAY CHAR(200),
#          DATUM CHAR(200),
#          NAME CHAR(200),
#          IBAN CHAR(200),
#          BIC CHAR(200),
#          NOTES CHAR(500)
#         );'''
#         )

conn.commit()

conn.close()
