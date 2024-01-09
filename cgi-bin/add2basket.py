#!/usr/bin/env python3.5
#add or remove an item from the shopping basket

#external librarys
from os import environ
import cgi

#internal librarys
from session import *
from functions import sendto

#useful variables
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

if GET["oppr"].value == 'cancel':
	SESSION.clear(item)

sendto(environ["HTTP_REFERER"])
