#some functions that can be used by all other cgi scripts
from os import environ
from http import cookies

def loadpage(name):
	myfile=open("pages/"+name,"r")
	returnme=myfile.read()
	myfile.close

	return returnme

def loadheader():
	returnme=loadpage("common_header.html")
	COOKIES=load_cookies()

	if COOKIES.get("Login_UID"):
		logout=loadpage("logout-form.html")
		returnme=returnme.replace("%LOGIN_BOX%",logout)
	else:
		login=loadpage("login-form.html")
		returnme=returnme.replace("%LOGIN_BOX%",login)

	return returnme

def load_cookies():
	COOKIES=cookies.SimpleCookie()
	COOKIES.load(environ["HTTP_COOKIE"])
	return COOKIES

def sendto(page,message=None):
	print("Content-type: text/html\n")

	if message:
		popup=loadpage("popup.html")
		popup=popup.replace("%MESSAGE%",message)
		print(popup)

	redirect_code=loadpage("redirect.html")
	redirect_code=redirect_code.replace("%GOTO_PAGE%",page)
	print(redirect_code)
