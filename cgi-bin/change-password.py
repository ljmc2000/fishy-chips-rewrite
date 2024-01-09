#!/usr/bin/env python3.5
#a script to allow the user to change their password

#internal libs
from functions import load_cookies,sendto
from database_connection import database_connect
from verify_password import verify_password
from classes import User

#external libs
import cgi
from os import environ
import bcrypt

#get cookies
COOKIES=load_cookies()

#ensure user is logged in
if COOKIES.get("Login_UID"):
	user=User(COOKIES["Login_UID"].value)

#get post data
POST=cgi.FieldStorage()
oldpwd=POST["oldpwd"].value
newpwd1=POST["newpwd1"].value
newpwd2=POST["newpwd2"].value

#get old password from database
myconnection,mycursor=database_connect()
getoldpassword="select password from users where(username=?)"
mycursor.execute(getoldpassword,(user.username,) )
(hashedword,)=mycursor.fetchone()
hashedword=hashedword.decode()

#check old password
if not verify_password(oldpwd,hashedword):
	sendto(environ["HTTP_REFERER"],message="wrong original password")
	quit()

#check passwords match
if newpwd1 != newpwd2:
	sendto(environ["HTTP_REFERER"],message="passwords don't match")
	quit()

#generate new password
newhashword=bcrypt.hashpw(newpwd1.encode(),bcrypt.gensalt())

#push to database
change_password="update users set password=? where (username=?)"
mycursor.execute(change_password,(newhashword,user.username) )
myconnection.commit()

#send user back
sendto(environ["HTTP_REFERER"],message="Password updated sucessfully")

