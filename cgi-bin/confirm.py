#!/usr/bin/python3.5
#confirm the users order at the checkout

#internal libs
from session import session_start
from database_connection import database_connect
from classes import User,CreditCard,Address
from functions import load_cookies,sendto

#external libs
from os import environ
import mysql.connector

#page vars
SESSION=session_start()
COOKIES=load_cookies()
lastpage=environ["HTTP_REFERER"]

#ensure user is logged in
if COOKIES.get("Login_UID"):
	user=User(COOKIES["Login_UID"].value)
else:
	sendto(lastpage,message="please login before ordering")
	quit()

#ensure user has a card and address
try:
	CreditCard(user.username)
	Address(user.username)
except mysql.connector.errors.ProgrammingError:
	sendto(lastpage,message="Only users with a registered credit card and address may order")
	quit()

#get item ids and prices
myconnection,mycursor=database_connect()
getids="select menunumber,price from food"
mycursor.execute(getids)
foodict=dict( mycursor.fetchall() )

#create string of items ordered, simultianiously calculating the total to be paid
items_ordered=""
total=0

for item in foodict:
	food="food"+str(item)
	if SESSION[food]:
		items_ordered = items_ordered + "%dx%s:" % (item,SESSION[food])
		total=total + (int(SESSION[food])*foodict[item])

#ensure a non blank order string
if items_ordered == "":
	sendto(lastpage,"Please order at least one item")
	quit()

#add order to database
try:
	makeorder="insert into orders (username,items_ordered,total,fulfilled) values (?,?,?,0)"
	mycursor.execute(makeorder,(user.username,items_ordered,total))
	myconnection.commit()
except:
	sendto(lastpage,"There was a problem with your order")
	quit()

mycursor.close()
myconnection.close()

#clear session
for item in foodict:
	food="food"+str(item)
	if SESSION[food]:
		SESSION.clear(food)

sendto("/","Your order has been placed sucessfully: Please allow 10-20 minutes for delivery. Remember to provide credit card information and delivery address or your order will fail to show up on our system")
