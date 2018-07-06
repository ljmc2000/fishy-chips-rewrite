#!/usr/bin/python3.5
#replace the image of a food

#internal libs
from database_connection import database_connect
from functions import is_admin,sendto

#external libs
import cgi
from os import environ

#check user is admin
if not is_admin:
	sendto("/",message="Access denied")

#page variables
POST=cgi.FieldStorage()
menunumber=POST["menunumber"].value
filename=POST["picture"].filename

#update database
update_picture="update food set picture=? where (menunumber=?)"
myconnection,mycursor=database_connect()
mycursor.execute(update_picture, (filename,menunumber) )

#update file
try:
	outfile=open("food_images/"+filename,"wb+")
	outfile.write(POST["picture"].value)
	myconnection.commit()
	mycursor.close()
	myconnection.close()
except:
	myconnection.rollback()
	sendto(environ["HTTP_REFERER"],message="updating picture failed")
	quit()

#return user to last page
sendto(environ["HTTP_REFERER"],message="menu entry updated")
