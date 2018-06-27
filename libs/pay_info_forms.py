#functions to print the forms for updating or adding payment info and address
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
		formstring=formstring.replace("%CCV%","%3d" % ccv)

	except TypeError:
		formstring=formstring.replace("%CARDNUMBER%","")
		formstring=formstring.replace("%EXPIREMONTH%","blank")
		formstring=formstring.replace("%EXPIREYEAR%","")
		formstring=formstring.replace("%CCV%","")

	mycursor.close()
	myconnection.close()
	return formstring

def gen_address_form(username):
	formstring=loadsubpage("delivery-address-form.html")
	myconnection,mycursor=database_connect()
	getaddress="select line1,line2,town,eircode from address where (username = ?)"

	mycursor.execute(getaddress,(username,))

	try:
		line1,line2,address,eircode=mycursor.fetchone()

		formstring=formstring.replace("%LINE1%",line1.decode() )
		formstring=formstring.replace("%LINE2%",line2.decode() )
		formstring=formstring.replace("%TOWN%",address.decode() )
		formstring=formstring.replace("%EIRCODE%",eircode.decode() )

	except TypeError:
		formstring=formstring.replace("%LINE1%","")
		formstring=formstring.replace("%LINE2%","blank")
		formstring=formstring.replace("%TOWN%","")
		formstring=formstring.replace("%EIRCODE%","")

	mycursor.close()
	myconnection.close()
	return formstring
