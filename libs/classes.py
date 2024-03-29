#classes to represent users, creditcards, addresses, Foods etc...

#internal libs
from database_connection import database_connect
from functions import loadpage,loadsubpage
from session import *
SESSION=session_start()

#external libs
from html import escape

class User:
	def __init__(self,uid):
		(myconnection,mycursor)=database_connect()
		get_user_details="select username from logged_in_users where(Login_UID=?)"
		mycursor.execute(get_user_details,(uid,))

		try:
			username, = mycursor.fetchone()
			mycursor.close()
			myconnection.close()

			self.username=username.decode()

		except TypeError:	#if user actually not logged in, destroy their login cookie
			#internal libs
			from functions import load_cookies,sendto
			#external libs
			from os import environ

			COOKIES=load_cookies()
			COOKIES["Login_UID"]["expires"]=-1
			print(COOKIES)
			sendto(environ["HTTP_REFERER"],message="Error with login cookie")
			quit()


	def __str__(self):
		return self.username

class CreditCard:
	def __init__(self,user):
		(myconnection,mycursor)=database_connect()
		get_credit_card="select cardnumber, expiremonth, expireyear, ccv from payinfo where (username=?)"
		mycursor.execute(get_credit_card,(user,))

		cardnumber, expiremonth, expireyear, ccv = mycursor.fetchone()
		mycursor.close()
		myconnection.close()

		self.cardnumber=cardnumber.decode()
		self.expiremonth=expiremonth.decode()
		self.expireyear=expireyear
		self.ccv=ccv

	def __str__(self):
		returnme=""
		returnme=returnme+"card_number: "+self.cardnumber+"\n"
		returnme=returnme+"expires: "+self.expiremonth+"/"+str(self.expireyear)+"\n"
		returnme=returnme+"CCV: "+str(self.ccv)
		return escape(returnme)

	def delimit(self,pagestring):
		pagestring=pagestring.replace("%CARD_NUMBER%",self.cardnumber)
		pagestring=pagestring.replace("%EXPIREMONTH%",self.expiremonth)
		pagestring=pagestring.replace("%EXPIREYEAR%",str(self.expireyear) )
		pagestring=pagestring.replace("%CCV%",str(self.ccv) )

		return pagestring

class Address:
	def __init__(self,user):
		(myconnection,mycursor)=database_connect()
		get_address="select line1, line2, town, eircode from address where (username=?)";
		mycursor.execute(get_address,(user,))

		line1, line2, town, eircode = mycursor.fetchone()
		mycursor.close()
		myconnection.close()

		self.line1=line1.decode()
		self.line2=line2.decode()
		self.town=town.decode()
		self.eircode=eircode.decode()

	def __str__(self):
		returnme=""
		returnme=returnme+self.line1+"\n"
		returnme=returnme+self.line2+"\n"
		returnme=returnme+self.town+"\n"
		returnme=returnme+self.eircode
		return escape(returnme)

	def delimit(self,pagestring):
		pagestring=pagestring.replace("%LINE1%",self.line1)
		pagestring=pagestring.replace("%LINE2%",self.line2)
		pagestring=pagestring.replace("%TOWN%",self.town)
		pagestring=pagestring.replace("%EIRCODE%",self.eircode)

		return pagestring

class Food:
	def __init__(self, menunumber, name, description, price, picture):
		self.menunumber=menunumber
		self.name=name
		self.description=description
		self.price=price
		self.picture=picture

	def asrow(self):
		'''print the class as a row in a table'''
		returnme=loadsubpage("index_table_row.html")
		returnme=self.delimit(returnme,short=True)
		return returnme

	def delimit(self,pagestring,short=False,hascur=True):
		'''replace each variable in pagestring with it\'s respective element of this class '''
		pagestring=pagestring.replace("%PICTURE%",self.picture)
		pagestring=pagestring.replace("%MENUNUMBER%","%d" % self.menunumber)
		pagestring=pagestring.replace("%NAME%",self.name)

		if hascur:
			pagestring=pagestring.replace("%PRICE%","€%.2f" % self.price)
		else:
			pagestring=pagestring.replace("%PRICE%","%.2f" % self.price )

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
