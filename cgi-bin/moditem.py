#!/usr/bin/env python3.5
#edit menuentries

#internal libs
from functions import *
from classes import loadfood

#external libs
import cgi

#page variables
COOKIES=load_cookies()
GET=cgi.FieldStorage()

#check user is admin
if not is_admin():
	sendto("/",message="Access Denied")
	quit()

#prepare the page for the client
pagestring=loadpage("moditem.html")
pagestring=pagestring.replace("%COMMON_HEADER%",loadheader() )
menuitem=loadfood(GET["menunumber"].value)
pagestring=menuitem.delimit(pagestring,hascur=False)

#send page to user
declare_http()
print(pagestring)
