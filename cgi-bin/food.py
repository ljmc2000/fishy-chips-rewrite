from database_connection import database_connect
from functions import loadpage
from session import *
SESSION=session_start()

class Food:
	def __init__(self, menunumber, name, description, price, picture):
		self.menunumber=menunumber
		self.name=name
		self.description=description
		self.price=price
		self.picture=picture

	def asrow(self):
		'''print the class as a row in a table'''
		returnme=loadpage("index_table_row.html")
		returnme=returnme.replace("%IMAGE%",self.picture)
		returnme=returnme.replace("%MENUNUMBER%","%d" % self.menunumber)
		returnme=returnme.replace("%NAME%",self.name)
		returnme=returnme.replace("%DESCRIPTION%",self.shortDescription())
		returnme=returnme.replace("%PRICE%","%.2f" % self.price)

		item="food"+str(self.menunumber)
		if item in SESSION:
			returnme=returnme.replace("%INBASKET%", "("+SESSION[item]+")" )
		else:
			returnme=returnme.replace("%INBASKET%","")

		return returnme

	def apply(self,pagestring,short=False):
		'''replace each variable in pagestring with it\'s respective element of this class '''
		pagestring=pagestring.replace("%PICTURE%","/food_images/"+self.picture)
		pagestring=pagestring.replace("%MENUNUMBER%","%d" % self.menunumber)
		pagestring=pagestring.replace("%NAME%",self.name)
		pagestring=pagestring.replace("%PRICE%","%.2f" % self.price)

		if short:
			pagestring=pagestring.replace("%DESCRIPTION%",self.shortDescription())
		else:
			pagestring=pagestring.replace("%DESCRIPTION%",self.description)

		item="food"+str(self.menunumber)
		if item in SESSION:
			pagestring=pagestring.replace("%INBASKET%", "("+SESSION[item]+")" )
		else:
			pagestring=pagestring.replace("%INBASKET%","")

		return pagestring


	def shortDescription(self):
		if len(self.description)>100:
			return self.description[:100]+"..."
		else:
			return self.description

def loadfood(menunumber):
	#request data from database
	myconnection,mycursor=database_connect()
	getfood="select menunumber,name,description,price,picture from food where(menunumber=?)"
	mycursor.execute(getfood,(menunumber,))

	#put data in vars
	menunumber,name,description,price,picture = mycursor.fetchone()
	mycursor.close()
	myconnection.close()

	#decode the unicode objects
	name=name.decode()
	description=description.decode()
	picture=picture.decode()

	return Food(menunumber,name,description,price,picture)


def make_menu():
	myconnection,mycursor=database_connect()
	getfood="select menunumber,name,description,price,picture from food"
	mycursor.execute(getfood)

	menu=[]
	for menunumber,name,description,price,picture in mycursor:
		name=name.decode()
		description=description.decode()
		picture=picture.decode()
		menu.append( Food(menunumber,name,description,price,picture) )

	mycursor.close()
	myconnection.close()

	return menu


def menu2string(menu):
	'''print a menu in index.py'''
	returnme="<table align=\"center\">"
	listsize=len(menu)
	for i in range(0,listsize,2):
		returnme=returnme+"<tr>"
		returnme=returnme+menu[i].asrow()
		if i<listsize-1:
			returnme=returnme+menu[i+1].asrow()
		returnme=returnme+"</tr>"
	returnme=returnme+"</table>"

	return returnme
