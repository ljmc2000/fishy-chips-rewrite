#!/usr/bin/python3
from functions import *

#load the page
pagestring=loadpage("index.html")


#send processed page to user
print("Content-Type: text/html\n")
print(pagestring)
