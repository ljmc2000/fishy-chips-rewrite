#I was messing around with cgi scripts and I couldn't find a native equivilant to phps $_SESSION variable
#so I made one myself


import os
from time import time
from http import cookies
from hashlib import sha512

#create session folder
directory=os.environ["TMPDIR"]+'/pysession/'
if not os.path.exists(directory):
	os.makedirs(directory)

class Session():
	def __init__(self,sid):
		if not sid:	#if no sid given
			now=str(time())
			now=now.encode()
			hashsid=sha512()
			hashsid.update(now)
			self.sid=hashsid.hexdigest()

		else:
			self.sid=sid

		#create folder for users session
		self.sessdir=directory+"/"+self.sid
		if not os.path.exists(self.sessdir):
			os.makedirs(self.sessdir)

		#make the object convertable to a dictionary
		self.__dict__=self.__dict__()

	def values(self):	#list all available keys
		return os.listdir(self.sessdir)

	def __str__(self):
		return str(self.__dict__)

	def __repr__(self):
		return "<Session object with sid "+self.sid+">"

	def __getitem__(self,key):
		try:
			file=open(self.sessdir+"/"+key,"r")
			returnme=file.readline()
			file.close()
		except FileNotFoundError:
			returnme=None

		return returnme

	def __setitem__(self,key,value):
		try:
			file=open(self.sessdir+"/"+key,"w+")
			file.write(value)
			self.__dict__=self.__dict__() #update the dictionary
		except TypeError:
			file.write("")

		return

	def __iter__(self):
		for item in os.listdir(self.sessdir):
			yield item

	def __dict__(self):
		returnme={}
		for item in self:
			returnme[item]=self[item]
		return returnme

def session_start():
	COOKIE=cookies.SimpleCookie()
	COOKIE.load(os.environ.get('HTTP_COOKIE'))

	if not COOKIE.get("SESSION"):
		SESSION=Session(None)
		COOKIE["SESSION"]=SESSION
		print(COOKIE)

	else:
		SESSION=Session(COOKIE["SESSION"].value)

	return SESSION

def session_destroy():
	COOKIE=cookies.SimpleCookie()
	COOKIE.load(os.environ.get('HTTP_COOKIE'))
	COOKIE["SESSION"]["expires"]=-1
	print(COOKIE)

	for file in os.listdir(directory+COOKIE["SESSION"].value):
		os.remove(directory+COOKIE["SESSION"].value+"/"+file)
	os.removedirs(directory+COOKIE["SESSION"].value+"/")
