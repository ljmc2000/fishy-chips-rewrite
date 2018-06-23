#!/usr/bin/python
#a page for creating a new user

#internal librarys
from functions import *

pagestring=loadpage("register.html")
pagestring=pagestring.replace("%COMMON_HEADER%", loadheader() )

print("Content-type: text/html\n")
print(pagestring)
