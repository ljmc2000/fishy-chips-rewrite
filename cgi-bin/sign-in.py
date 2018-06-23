#!/usr/bin/python3

#internal librarys
from database_connection import database_connect
from functions import *
from verify_password import verify_password

#external librarys
from hashlib import sha256
from time import time,localtime,strftime
from os import environ
import bcrypt,cgi

myconnection,mycursor=database_connect()
cookie_expiry=60*60*24*30	#keep the cookie for 30 days
now=time()
COOKIES=load_cookies()

#get username and password from post request
POST=cgi.FieldStorage()
try:
	username=POST["username"].value
	password=POST["password1"].value

except KeyError: #ensure correct post data
	sendto("/",message="Username or password blank")
	quit()

#get password hash from database
try:
	getLoginData="select password from users where username=?"
	mycursor.execute(getLoginData,(username,))
	(hashword,) = mycursor.fetchone()
	hashword=hashword.decode()

except TypeError:
	sendto("/",message="User %s not found" % username)
	quit()

#verify password hash
if not verify_password(password,hashword):
	sendto("/",message="password is wrong")
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
expires=strftime('%Y-%m-%d %H:%M:%S',localtime(now+cookie_expiry))
mycursor.execute(savecookie, (username,Login_UID,expires,))
myconnection.commit()

#redirect user to welcome page
sendto("/")

#close connection and cursor
mycursor.close()
myconnection.close()
