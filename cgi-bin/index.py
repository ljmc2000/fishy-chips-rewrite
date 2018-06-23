#!/usr/bin/python3
#the "homepage" of the website

#internal librarys
from functions import *
from food import make_menu,menu2string

#load the page
pagestring=loadpage("index.html")
common_header=loadheader()

#create the page the user wants to see
pagestring=pagestring.replace("%COMMON_HEADER%",common_header)
pagestring=pagestring.replace("%FOODTABLE%",  menu2string( make_menu() )  )

#send processed page to user
print("Content-Type: text/html\n")
print(pagestring)
