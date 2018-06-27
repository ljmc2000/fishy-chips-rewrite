#!/usr/bin/python3.5
#update payment info with a post request

#internal librarys
from database_connection import database_connect
from functions import load_cookies,sendto
from userclasses import User

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
cardnumber=POST["cardnum"].value
expiremonth=POST["expiremonth"].value
expireyear=POST["expireyear"].value
ccv=POST["ccv"].value


#open connection to database and prepare statement
if POST["expiremonth"].value != "cur":
	myconnection,mycursor=database_connect()
	add_pay_info="update payinfo set cardnumber=?, expiremonth=?, expireyear=?, ccv=? where (username=?)"
	mycursor.execute(add_pay_info,(cardnumber,expiremonth,expireyear,ccv,username))

else:
	myconnection,mycursor=database_connect()
	add_pay_info="update payinfo set cardnumber=?, expireyear=?, ccv=? where (username=?)"
	mycursor.execute(add_pay_info,(cardnumber,expireyear,ccv,username))

myconnection.commit()
mycursor.close()
myconnection.close()

sendto(environ["HTTP_REFERER"])
