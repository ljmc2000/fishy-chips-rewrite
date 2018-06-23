#!/usr/bin/python3

from http import cookies
from os import environ
from database_connection import database_connect
from functions import sendto

COOKIES=cookies.SimpleCookie()
COOKIES.load(environ["HTTP_COOKIE"])

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
