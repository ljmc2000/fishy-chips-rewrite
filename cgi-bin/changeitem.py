#!/usr/bin/python3.5
#modify an item from the menu

#internal libs
from functions import is_admin
from database_connection import database_connect

#external libs
import cgi

#ensure user is admin
if not is_admin:
	sendto("/",message="Access denied")

#page variables
POST=cgi.FieldStorage()
menunumber=POST["menunumber"].value
name=POST["name"].value
description=POST["description"].value
price=POST["price"].value

print("Content-type: text/plain\n")
print(menunumber,name,description,price)
