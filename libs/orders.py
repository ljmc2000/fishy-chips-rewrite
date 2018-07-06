#internal libs
from classes import Address
from functions import loadsubpage

#external libs
from html import escape

def get_order_tables():
	'''generate table of orders'''
	from database_connection import database_connect

	returnme=""
	row_template=loadsubpage("orders_table_row.html")
	myconnection,mycursor=database_connect()
	get_orders="select username,items_ordered,orderno from valid_orders where fulfilled=0"
	mycursor.execute(get_orders)

	for username,items_ordered,orderno in mycursor:
		row=row_template
		safeusername=escape( username.decode() )
		row=row.replace("%USERNAME%",safeusername )
#		row=row.replace("%ORDERED_ITEMS%",parse_order(items_ordered) )
		addr=str( Address( username.decode() ) )
		row=row.replace("%ADDRESS%",addr)

		returnme=returnme+row

	mycursor.close()
	myconnection.close()

	return returnme
