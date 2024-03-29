#!/usr/bin/env python3.5
#allow the user to modify or confirm their order

#internal libs
from functions import *
from checkout_funcs import *
from pay_info_forms import *
from classes import User

#load cookies
COOKIES=load_cookies()

#get user and ensure signed in
if COOKIES.get("Login_UID"):
	user=User(COOKIES["Login_UID"].value)
else:
	sendto("/")

#generate page
pagestring=loadpage("checkout.html")
pagestring=pagestring.replace("%COMMON_HEADER%",loadheader())
pagestring=pagestring.replace("%ITEMCART_TABLE%",gen_item_table())
pagestring=pagestring.replace("%PAYMENT_INFO_FORM%",gen_payment_info_form(user.username) )
pagestring=pagestring.replace("%DELIVERY_ADDRESS_FORM%",gen_address_form(user.username) )

#send page to user
declare_http()
print(pagestring)
