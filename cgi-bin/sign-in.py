#!/usr/bin/env python3.5
#allow the user to login

#internal librarys
from database_connection import database_connect
from functions import *
from verify_password import verify_password

#external librarys
from hashlib import sha256
import datetime
from os import environ
import bcrypt,cgi

myconnection,mycursor=database_connect()
cookie_expiry=60*60*24*30	#keep the cookie for 30 days
now=datetime.datetime.now()
COOKIES=load_cookies()
redirectpage=environ["HTTP_REFERER"]	#dont change page on login

#get username and password from post request
POST=cgi.FieldStorage()
try:
	username=POST["username"].value
	password=POST["password1"].value

except KeyError: #ensure correct post data
	sendto(redirectpage,message="Username or password blank")
	quit()

#get password hash from database
try:
	getLoginData="select password from users where username=?"
	mycursor.execute(getLoginData,(username,))
	(hashword,) = mycursor.fetchone()
	hashword=hashword.decode()

except TypeError:
	sendto(redirectpage,message="User %s not found" % username)
	quit()

#verify password hash
if not verify_password(password,hashword):
	sendto(redirectpage,message="password is wrong")
	quit()

#generate login uid
Login_UID=sha256()
Login_UID.update(str(now).encode())
Login_UID.update(bcrypt.gensalt())
Login_UID=Login_UID.hexdigest()

#send user the login cookie
COOKIES["Login_UID"]=Login_UID
COOKIES["Login_UID"]["expires"]=cookie_expiry
print(COOKIES)

#add the login cookie to the database
savecookie=("insert into logged_in_users values(?,?,?)")
expires=datetime.datetime.now() + datetime.timedelta(seconds=cookie_expiry)
mycursor.execute(savecookie, (username,Login_UID,expires,))
myconnection.commit()

#redirect user to where they started
sendto(redirectpage)

#close connection and cursor
mycursor.close()
myconnection.close()
