#I was messing around with cgi scripts and I couldn't find a native equivilant to phps $_SESSION variable
#so I made one myself


import os
from time import time
from http import cookies
from hashlib import sha512

#create session folder
try:
	directory=os.environ["TMPDIR"]+'/pysession/'
except KeyError:
	directory="/tmp/pysession/"

if not os.path.exists(directory):
	os.makedirs(directory,0o700)

class Session():
	'''an object to represent a php like session'''
	def __init__(self,sid):
		self.sid=sid

		#create folder for users session with mode 700
		self.sessdir=directory+"/"+self.sid
		if not os.path.exists(self.sessdir):
			os.makedirs(self.sessdir,0o700)

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

	def clear(self,key):
		'''wipe a key clean completely'''
		try:
			os.remove(self.sessdir+"/"+key)
		except FileNotFoundError:
			#do nothing
			pass

	def destroy(self):
		'''destroy the session object'''
		for key in os.listdir(self.sessdir):
			os.remove(self.sessdir+"/"+key)
		os.removedirs(self.sessdir)
		self.__class__=DestroyedSession

class DestroyedSession:
	'''a session that has been destroyed'''

	def __str__(self):
		raise TypeError("Session has been destroyed")

	def __repr__(self):
		return "<Destroyed Session object with sid "+self.sid+">"

	def __getitem__(self,key):
		raise TypeError("Session has been destroyed")

	def __setitem__(self,key,value):
		raise TypeError("Session has been destroyed")

	def __iter__(self):
		raise TypeError("Session has been destroyed")

	def __dict__(self):
		raise TypeError("Session has been destroyed")

	def clear(self,key):
		raise TypeError("Session has been destroyed")

def session_start():
	COOKIE=cookies.SimpleCookie()
	COOKIE.load(os.environ.get('HTTP_COOKIE'))

	if not COOKIE.get("SESSION"):
		now=str(time())
		now=now.encode()
		hashsid=sha512()
		hashsid.update(now)
		sid=hashsid.hexdigest()

		SESSION=Session(sid)
		COOKIE["SESSION"]=SESSION.sid
		print(COOKIE)

	else:
		SESSION=Session(COOKIE["SESSION"].value)

	return SESSION
