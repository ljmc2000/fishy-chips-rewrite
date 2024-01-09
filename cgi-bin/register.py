#!/usr/bin/env python3.5
#a page for creating a new user

#internal librarys
from functions import *

#redirect to homepage if already signed in
COOKIES=load_cookies()
if COOKIES.get("Login_UID"):
	sendto("/")

pagestring=loadpage("register.html")
pagestring=pagestring.replace("%COMMON_HEADER%", loadheader() )

declare_http()
print(pagestring)
