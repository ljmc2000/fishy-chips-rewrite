#!/usr/bin/python3.5
#mark an order fulfilled

#internal libs
from functions import is_admin,sendto
from database_connection import database_connect

#external libs
import cgi
from os import environ

#check admin
if not is_admin():
	sendto("/",message="access denied")
	quit()

#page vars
GET=cgi.FieldStorage()
orderno=GET["ordernumber"].value

#update database
myconnection,mycursor=database_connect()
set_fulfilled="update orders set fulfilled=1 where orderno=?"
mycursor.execute(set_fulfilled,(orderno,))
myconnection.commit()

mycursor.close()
myconnection.close()
sendto(environ["HTTP_REFERER"])
