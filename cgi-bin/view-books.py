#!/usr/bin/python3.5
#view gross profits for the business

#internal libs
from functions import *

#check admin
if not is_admin():
	sendto("/",message="access_denied")
	quit()

#genderate page
pagestring=loadpage("view-books.html")
pagestring=pagestring.replace("%COMMON_HEADER%",loadheader() )

#send page to user
declare_http()
print(pagestring)
