#!/usr/bin/python3.5
#View a list of outstanding orders

#internal libs
from functions import *
from orders import get_order_tables

#check user is admin
if not is_admin():
	sendto("/",message="access_forbidden")
	quit()

#prepare page to send to user
pagestring=loadpage("view-orders.html")
pagestring=pagestring.replace("%COMMON_HEADER%",loadheader() )
pagestring=pagestring.replace("%TABLE_ROWS%",get_order_tables() )

#send page to user
declare_http()
print(pagestring)
