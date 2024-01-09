#!/usr/bin/env python3.5
#cancel an order

#internal libs
from functions import sendto,load_cookies
from database_connection import database_connect
from classes import User

#external libs
import cgi
from os import environ

#pagevars
GET=cgi.FieldStorage()
COOKIES=load_cookies()

#check user is logged in
if COOKIES.get("Login_UID"):
	user=User(COOKIES["Login_UID"].value)

myconnection,mycursor=database_connect()
cancel_order="delete from orders where (orderno=? and username=? and fulfilled=0)"
mycursor.execute(cancel_order,(GET["ordernumber"].value,user.username))
myconnection.commit()

sendto(environ["HTTP_REFERER"],message="Order has been canceled")
