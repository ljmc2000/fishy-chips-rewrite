#!/usr/bin/python3
from functions import *

#load the page
pagestring=loadpage("index.html")
common_header=loadheader()

#create the page the user wants to see
pagestring=pagestring.replace("%COMMON_HEADER%",common_header)

#send processed page to user
print("Content-Type: text/html\n")
print(pagestring)
