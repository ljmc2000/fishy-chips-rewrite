#!/usr/bin/env python3.5
#modify an item from the menu

#internal libs
from functions import is_admin,sendto
from database_connection import database_connect

#external libs
import cgi
from os import environ

#ensure user is admin
if not is_admin():
	sendto("/",message="Access denied")
	quit()

#page variables
POST=cgi.FieldStorage()
menunumber=POST["menunumber"].value
name=POST["name"].value
description=POST["description"].value
price=POST["price"].value

#update database
update_item="update food set name=?,description=?,price=? where (menunumber=?)"
myconnection,mycursor=database_connect()
mycursor.execute(update_item,(name,description,price,menunumber))
myconnection.commit()

mycursor.close()
myconnection.close()

#return user to last page
sendto(environ["HTTP_REFERER"],message="menu entry updated")
