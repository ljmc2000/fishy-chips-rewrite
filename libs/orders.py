#librarys to do with displaying orders

#internal libs
from classes import Address
from functions import loadsubpage

#external libs
from html import escape

def parse_order(items_ordered):
	'''convert an order string to a human readable order'''
	#internal libs
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

	mycursor.close()
	myconnection.close()
	return returnme

def cancel_button(orderid):
	#internal libs
	from functions import loadsubpage

	returnme=loadsubpage("cancel_button.html")
	returnme=returnme.replace("%ORDER_ID%","%d" % orderid)
	return returnme

def get_order_tables():
	'''generate table of orders'''
	#internal libs
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
		row=row.replace("%ORDERNO%", str(orderno) )

		returnme=returnme+row

	mycursor.close()
	myconnection.close()

	return returnme

def get_user_order_table(username):
	'''generate a table of orders for a specific user'''
	#internal libs
	from database_connection import database_connect

	returnme=""
	row_template=loadsubpage("user_orders_table_row.html")
	myconnection,mycursor=database_connect()
	get_orders="select placed, items_ordered, total, orderno, fulfilled from orders where username=?"
	mycursor.execute(get_orders,(username,))

	for placed, items_ordered, total, orderno, fulfilled in mycursor:
		row=row_template
		row=row.replace("%PLACED%", placed.strftime("%d/%B/%Y<br>%H:%M") )
		row=row.replace("%ORDERED_ITEMS%",parse_order(items_ordered) )
		row=row.replace("%TOTAL%","€%.2f" % total)

		if not fulfilled:
			row=row.replace("%CANCEL_BUTTON%",cancel_button(orderno) )
		else:
			row=row.replace("%CANCEL_BUTTON%","")

		returnme=returnme+row

	return returnme
