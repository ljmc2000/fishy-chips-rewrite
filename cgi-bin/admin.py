#!/usr/bin/python3.5
#let the admin modify the menu or their password

#internal libraries
from functions import *

#check if user is admin
if not is_admin():
	sendto("/",message="Permission denied")
	quit()

#generate page
pagestring=loadpage("admin.html")


#send data to user
declare_http()
print(pagestring)
