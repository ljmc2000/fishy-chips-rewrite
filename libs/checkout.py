#functions for checking out

#internal functions
from functions import loadsubpage
from database_connection import database_connect
from session import *

def gen_item_table():
#	SESSION=session_start()
	SESSION=Session("12")

	myconnection,mycursor=database_connect()
	getitems="select menunumber, name, price from food"

	mycursor.execute(getitems)

	checkout_table_row=loadsubpage("checkout_table_row.html")
	returnme=""

	for menunumber, name, price in mycursor:
		menunumber=str(menunumber)
		if "food"+menunumber in SESSION:
			row=checkout_table_row
			row=row.replace("%MENUNUMBER%",menunumber)
			row=row.replace("%NAME%",name.decode() )
			row=row.replace("%INBASKET%",SESSION["food"+menunumber])
			row=row.replace("%PRICE%", "€%.2f" % price)
			returnme=returnme+row

	mycursor.close()
	myconnection.close()

	return returnme
