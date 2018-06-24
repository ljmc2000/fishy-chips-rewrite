#!/usr/bin/python3.5
#allow the user to logout

#external libraries
from os import environ

#internal libraries
from database_connection import database_connect
from functions import sendto,load_cookies
COOKIES=load_cookies()


if not COOKIES.get("Login_UID"):
	sendto("/",message="Not signed in")
else:
	myconnection,mycursor=database_connect()

	logout=("delete from logged_in_users where(Login_UID=?)")
	mycursor.execute(logout,(COOKIES["Login_UID"].value,))
	myconnection.commit()
	COOKIES["Login_UID"]["expires"]=-1
	print(COOKIES)
	sendto("/")

	mycursor.close()
	myconnection.close()
