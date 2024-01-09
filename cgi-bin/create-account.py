#!/usr/bin/env python3.5
#create a user account from a post request

#internal functions
from functions import sendto,load_cookies
from database_connection import database_connect

#external functions
import cgi, bcrypt
from mysql.connector import errors

#useful variables
COOKIES=load_cookies()
POST=cgi.FieldStorage()

#get username and password from post request
try:
	username=POST["username"].value
	password1=POST["password1"].value
	password2=POST["password2"].value

except KeyError: #ensure correct post data
	sendto("/cgi-bin/register.py",message="Username or password blank")
	quit()

#check passwords match
if password1 != password2:
	sendto("/cgi-bin/register.py",message="Passwords do not match")
	quit()

#encrypt the password
hashword=bcrypt.hashpw(password1.encode(), bcrypt.gensalt() )

#add user to database
myconnection,mycursor=database_connect()

try:
	addnewuser="insert into users values(?,?)"
	mycursor.execute(addnewuser,(username,hashword))
	myconnection.commit()

except errors.IntegrityError:
	sendto("/cgi-bin/register.py",message="Pre existing user found")

mycursor.close()
myconnection.close()

sendto("/")
