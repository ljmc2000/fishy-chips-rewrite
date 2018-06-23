#!/usr/bin/python3
from functions import *
from food import 

pagestring=loadpage("itempage.html")
pagestring=pagestring.replace("%COMMON_HEADER%", loadheader() )

#serve page to user
print("Content-type: text/html\n")
print(pagestring)
