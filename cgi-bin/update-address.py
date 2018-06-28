#!/usr/bin/python3.5
#update payment info with a post request

#internal librarys
from database_connection import database_connect
from functions import load_cookies,sendto
from classes import User

#external libs
import cgi
from os import environ

#initialise POST and cookies
POST=cgi.FieldStorage()
COOKIES=load_cookies()

#ensure user is logged in
if COOKIES.get("Login_UID"):
	user=User(COOKIES["Login_UID"].value)

#get info to insert into database
username=user.username
line1=POST["line1"].value
town=POST["town"].value
eircode=POST["eircode"].value

#add line2 to info if not null
try:
	line2=POST["line2"].value
except KeyError:
	line2=""

#open connection to database and prepare statement
myconnection,mycursor=database_connect()
add_address="update address set line1=?, line2=?, town=?, eircode=? where (username=?)"
mycursor.execute(add_address,(line1,line2,town,eircode,username))

myconnection.commit()
mycursor.close()
myconnection.close()

sendto(environ["HTTP_REFERER"])
