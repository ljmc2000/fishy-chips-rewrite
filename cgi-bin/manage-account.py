#!/usr/bin/python3.5
#allow the user to cancel orders, change passwords or change and delete payment info/address

#internal libs
from functions import *
from classes import User
from pay_info_forms import gen_payment_info_form,gen_address_form

#page vars
COOKIES=load_cookies()

#get user and ensure signed in
if COOKIES.get("Login_UID"):
	user=User(COOKIES["Login_UID"].value)
else:
	sendto("/",message="please login to manage your account")

#generate page
pagestring=loadpage("manage-account.html")
pagestring=pagestring.replace("%COMMON_HEADER%",loadheader() )
pagestring=pagestring.replace("%PAYMENT_INFO_FORM%",gen_payment_info_form(user.username) )
pagestring=pagestring.replace("%DELIVERY_ADDRESS_FORM%",gen_address_form(user.username) )

#send page to user
declare_http()
print(pagestring)
