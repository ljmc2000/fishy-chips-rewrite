#!/usr/bin/python3
#a page where the item description may be read in full if too long
from functions import *
from food import *
import cgi

GET=cgi.FieldStorage()
menunumber=GET["menunumber"].value
food=loadfood(menunumber)

#generate the page
pagestring=loadpage("itempage.html")
pagestring=pagestring.replace("%COMMON_HEADER%", loadheader() )
pagestring=food.delimit(pagestring)

#serve page to user
print("Content-type: text/html\n")
print(pagestring)
