#functions only to be used by admin
from functions import loadsubpage
from database_connection import database_connect

def get_modlink_items():
	'''list of foods with options to modify or delete them'''
	modlink_items=loadsubpage("modlink_items.html")
	myconnection,mycursor=database_connect()
	get_items="select name,menunumber from food"
	mycursor.execute(get_items)

	returnme=""
	for (name,menunumber) in mycursor:
		line=modlink_items
		line=line.replace("%NAME%",name.decode() )
		line=line.replace("%MENUNUMBER%",str(menunumber) )
		returnme=returnme+line

	mycursor.close()
	myconnection.close()

	return returnme
