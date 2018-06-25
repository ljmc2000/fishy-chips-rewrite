#functions for checking out

#internal functions
from functions import loadsubpage
from database_connection import database_connect
from session import *

def gen_item_table():
	SESSION=session_start()

	myconnection,mycursor=database_connect()
	getitems="select menunumber, name, price from food"

	mycursor.execute(getitems)

	checkout_table_row=loadsubpage("checkout_table_row.html")
	returnme=loadsubpage("checkout_table_head.html")
	total=0

	for menunumber, name, price in mycursor:
		menunumber=str(menunumber)
		if "food"+menunumber in SESSION:
			inbasket=SESSION["food"+menunumber]
			batch_price=price*int(SESSION["food"+menunumber])
			total=total+batch_price

			row=checkout_table_row
			row=row.replace("%MENUNUMBER%",menunumber)
			row=row.replace("%NAME%",name.decode() )
			row=row.replace("%INBASKET%",inbasket)
			row=row.replace("%BATCH_PRICE%", "€%.2f" % batch_price)
			returnme=returnme+row

	tail=loadsubpage("checkout_table_tail.html")
	tail=tail.replace("%TOTAL%","€%.2f" % total)
	returnme=returnme+tail

	mycursor.close()
	myconnection.close()

	return returnme
