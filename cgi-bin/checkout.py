#!/usr/bin/python3.5
#allow the user to modify or confirm their order

#internal libs
from functions import loadpage,loadheader,declare_http
from checkout_funcs import *
from pay_info_forms import *
from userclasses import User

#external libs
from http import cookies
from os import environ

#load cookies
COOKIES=cookies.SimpleCookie()
COOKIES.load(environ["HTTP_COOKIE"])

#get user
user=User(COOKIES["Login_UID"].value)

#generate page
pagestring=loadpage("checkout.html")
pagestring=pagestring.replace("%COMMON_HEADER%",loadheader())
pagestring=pagestring.replace("%ITEMCART_TABLE%",gen_item_table())
pagestring=pagestring.replace("%PAYMENT_INFO_FORM%",gen_payment_info_form(user.username) )

#send page to user
declare_http()
print(pagestring)
