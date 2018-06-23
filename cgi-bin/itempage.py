#!/usr/bin/python3
from functions import *
from food import *
import cgi

GET=cgi.FieldStorage()
menunumber=GET["menunumber"].value
food=loadfood(menunumber)

#generate the page
pagestring=loadpage("itempage.html")
pagestring=pagestring.replace("%COMMON_HEADER%", loadheader() )
pagestring=food.apply(pagestring)

#serve page to user
print("Content-type: text/html\n")
print(pagestring)
