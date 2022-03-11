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



#conn.execute(
#        '''CREATE TABLE ADDENDA
#         (
#		  NAME CHAR(500),
#          DATE CHAR(20),
#          ISDELETE CHAR(20)
#         );'''
#         )

conn.commit()

conn.close()
