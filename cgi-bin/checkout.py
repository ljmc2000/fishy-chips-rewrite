#!/usr/bin/python3.5
#allow the user to modify or confirm their order

#internal libs
from session import *
from functions import loadpage,loadheader,declare_http
from checkout_funcs import *

#generate page
pagestring=loadpage("checkout.html")
pagestring=pagestring.replace("%COMMON_HEADER%",loadheader())
pagestring=pagestring.replace("%ITEMCART_TABLE%",gen_item_table())

#send page to user
declare_http()
print(pagestring)
