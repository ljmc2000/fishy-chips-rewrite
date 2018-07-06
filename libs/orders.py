#librarys to do with displaying orders

#internal libs
from classes import Address
from functions import loadsubpage

#external libs
from html import escape

def parse_order(items_ordered):
	'''convert an order string to a human readable order'''
	from database_connection import database_connect

	items_ordered=items_ordered.decode().strip(":")

	foodict={}
	getfoods="select menunumber,name from food"
	myconnection,mycursor=database_connect()
	mycursor.execute(getfoods)

	for menunumber,name in mycursor:
		foodict[menunumber]=name.decode()

	returnme=""
	for line in items_ordered.split(":"):
		line=line.split("x")
		line[0]=int(line[0])
		returnme=returnme+foodict[ line[0] ]+"×"+line[1]+"<br>"

	return returnme

def get_order_tables():
	'''generate table of orders'''
	from database_connection import database_connect

	returnme=""
	row_template=loadsubpage("orders_table_row.html")
	myconnection,mycursor=database_connect()
	get_orders="select username,placed,items_ordered,orderno from valid_orders where fulfilled=0"
	mycursor.execute(get_orders)

	for username,placed,items_ordered,orderno in mycursor:
		row=row_template
		safeusername=escape( username.decode() )
		row=row.replace("%USERNAME%",safeusername )
		row=row.replace("%PLACED%", placed.strftime("%H:%M") )
		row=row.replace("%ORDERED_ITEMS%",parse_order(items_ordered) )
		addr=str( Address( username.decode() ) ).replace("\n","<br>")
		row=row.replace("%ADDRESS%",addr)

		returnme=returnme+row

	mycursor.close()
	myconnection.close()

	return returnme
