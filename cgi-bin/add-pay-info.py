#!/usr/bin/python3.5
#add new payment info with a post request

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
cardnumber=POST["cardnum"].value
expiremonth=POST["expiremonth"].value
expireyear=POST["expireyear"].value
ccv=POST["ccv"].value


#open connection to database and prepare statement
myconnection,mycursor=database_connect()
add_pay_info="insert into payinfo (username,cardnumber,expiremonth,expireyear,ccv) values(?,?,?,?,?)"
mycursor.execute(add_pay_info,(username,cardnumber,expiremonth,expireyear,ccv))

myconnection.commit()
mycursor.close()
myconnection.close()

sendto(environ["HTTP_REFERER"])
