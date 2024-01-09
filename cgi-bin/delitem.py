#!/usr/bin/env python3.5
#delete an item from the menu

#external functions
import cgi, os

#internal functions
from functions import is_admin,sendto
from database_connection import database_connect

#http vars
GET=cgi.FieldStorage()
menunumber=GET["menunumber"].value

#check user is administrator
if not is_admin():
	sendto("/",message="Permission denied")
	quit()

#sql connection
myconnection,mycursor=database_connect()

#delete picture from storage
getpic="select picture from food where (menunumber=?)"
mycursor.execute(getpic,(menunumber,))
filename,=mycursor.fetchone()
try:
	filename=filename.decode()
	os.remove("food_images/"+filename)
except FileNotFoundError:
	pass

#delete food from database
delitem="delete from food where (menunumber=?)"
mycursor.execute(delitem,(menunumber,))
myconnection.commit()

sendto("/cgi-bin/admin.py")

#close database connection
mycursor.close()
myconnection.close()
