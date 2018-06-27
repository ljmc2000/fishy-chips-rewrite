#functions to print the forms for updating or adding payment info
from functions import loadsubpage
from database_connection import database_connect

def gen_payment_info_form(username):
	formstring=loadsubpage("payment-info-form.html")
	myconnection,mycursor=database_connect()
	getpayinfo="select cardnumber,expiremonth,expireyear,ccv from payinfo where (username = ?)"

	mycursor.execute(getpayinfo,(username,))

	try:
		cardnumber,expiremonth,expireyear,ccv=mycursor.fetchone()

		formstring=formstring.replace("%CARDNUMBER%",cardnumber.decode())
		formstring=formstring.replace("%EXPIREMONTH%",expiremonth.decode())
		formstring=formstring.replace("%EXPIREYEAR%","%2d" % expireyear)
		formstring=formstring.replace("%CCV%","%3d" % expireyear)

	except TypeError:
		formstring=formstring.replace("%CARDNUMBER%","")
		formstring=formstring.replace("%EXPIREMONTH%","blank")
		formstring=formstring.replace("%EXPIREYEAR%","")
		formstring=formstring.replace("%CCV%","")

	mycursor.close()
	myconnection.close()
	return formstring
