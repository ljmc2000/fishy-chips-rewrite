#!/usr/bin/env python3.5
#add an item to the menu

#internal functions
from functions import is_admin,sendto
from database_connection import database_connect

#external functions
import cgi

#ensure admin
if not is_admin():
	sendto("/",message="Access denied")
	quit()

#useful variables
POST=cgi.FieldStorage()
name=POST["name"].value
description=POST["description"].value
price=float(POST["price"].value)
filename=POST["picture"].filename

#add picture to storage
outfile=open("food_images/"+filename,"wb+")
outfile.write(POST["picture"].value)
outfile.close()

#add entry to database
myconnection,mycursor=database_connect()
putfood="insert into food(name,description,price,picture) values(?,?,?,?)"
mycursor.execute(putfood,(name,description,price,filename))
myconnection.commit()

mycursor.close()
myconnection.close()


#redirect user back to admin page
sendto("/cgi-bin/admin.py")
