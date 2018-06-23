from database_connection import database_connect
from functions import loadpage

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

		return returnme

	def shortDescription(self):
		if len(self.description)>100:
			return self.description[:100]+"..."
		else:
			return self.description

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

	return menu

def menu2string(menu):
	'''print a menu in index.py'''
	returnme=""
	listsize=len(menu)-1
	for i in range(0,listsize,2):
		returnme=returnme+"<tr>"
		returnme=returnme+menu[i].asrow()
		if i>=listsize:
			returnme=returnme+menu[i+1].asrow()
		returnme=returnme+"</tr>"

	return returnme