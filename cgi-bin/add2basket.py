#!/usr/bin/python3
from os import environ
from session import *
import cgi
from functions import sendto

SESSION=session_start()
GET=cgi.FieldStorage()


item="food"+GET["menunumber"].value

if GET["oppr"].value == 'a':
	if not SESSION[item]:
		SESSION[item]="1"
	else:
		SESSION[item]=str(int(SESSION[item])+1)

if GET["oppr"].value == '-':
	if SESSION[item]=="1":
		SESSION.clear(item)
	else:
		SESSION[item]=str(int(SESSION[item])-1)

sendto(environ["HTTP_REFERER"])