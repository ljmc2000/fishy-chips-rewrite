#!/usr/bin/python3.5
#a page for creating a new user

#internal librarys
from functions import *

pagestring=loadpage("register.html")
pagestring=pagestring.replace("%COMMON_HEADER%", loadheader() )

declare_http()
print(pagestring)
