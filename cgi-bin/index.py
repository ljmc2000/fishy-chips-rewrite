#!/usr/bin/env python3.5
#the "homepage" of the website

#internal librarys
from functions import *
from classes import make_menu,menu2string

#load the page
pagestring=loadpage("index.html")
common_header=loadheader()

#create the page the user wants to see
pagestring=pagestring.replace("%COMMON_HEADER%",common_header)
pagestring=pagestring.replace("%FOODTABLE%",  menu2string( make_menu() )  )

#send processed page to user
declare_http()
print(pagestring)
