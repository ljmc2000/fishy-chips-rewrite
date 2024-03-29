#!/usr/bin/env python3.5
#a page where the item description may be read in full if too long

#internal librarys
from functions import *
from classes import loadfood

#external librarys
import cgi

#initialise some data
GET=cgi.FieldStorage()
menunumber=GET["menunumber"].value
food=loadfood(menunumber)

#generate the page
pagestring=loadpage("itempage.html")
pagestring=pagestring.replace("%COMMON_HEADER%", loadheader() )
pagestring=food.delimit(pagestring)

#serve page to user
declare_http()
print(pagestring)
