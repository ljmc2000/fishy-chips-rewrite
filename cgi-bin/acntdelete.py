#!/usr/bin/python3.5
#allow the user to delete their credit card info or their address

#internal libs
from functions import sendto,load_cookies
from database_connection import database_connect

#external libs
import cgi
from os import environ
from classes import User

#page vars
GET=cgi.FieldStorage()
COOKIES=load_cookies()

#ensure user is logged in
if COOKIES["Login_UID"].get:
	user=User(COOKIES["Login_UID"].value)

#check for outstanding orders
myconnection,mycursor=database_connect()
check_orders="select count(orderno) from valid_orders where (fulfilled=0 and username=?)"
mycursor.execute(check_orders,(user.username,))
order_count,=mycursor.fetchone()
if order_count>0:
	sendto(environ["HTTP_REFERER"],message="You may not delete payment information with outstanding orders")

elif GET["field"].value == "payinfo":
	del_pay_info="delete from payinfo where username = ?"
	mycursor.execute( del_pay_info, (user.username,) )
	myconnection.commit()
	sendto(environ["HTTP_REFERER"])

elif GET["field"].value == "address":
	del_address="delete from address where username = ?"
	mycursor.execute( del_address, (user.username,) )
	myconnection.commit()
	sendto(environ["HTTP_REFERER"])

mycursor.close()
myconnection.close()
