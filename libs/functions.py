#some functions that can be used by all other cgi scripts
from os import environ
from http import cookies
from userclasses import User

def is_admin():
	'''check if the user is logged in and is an admin'''
	COOKIES=load_cookies()
	if not COOKIES.get("Login_UID"):
		return False

	user=User(COOKIES["Login_UID"].value)

	return user.username=="admin"

def loadpage(name):
	myfile=open("pages/"+name,"r")
	returnme=myfile.read()
	myfile.close

	return returnme

def loadheader():
	returnme=loadpage("common_header.html")
	COOKIES=load_cookies()

	if is_admin():
		admin_header=loadpage("admin-header.html")
		returnme=returnme.replace("%LOGIN_BOX%",admin_header)

	elif COOKIES.get("Login_UID"):
		logout=loadpage("logout-form.html")
		returnme=returnme.replace("%LOGIN_BOX%",logout)
	else:
		login=loadpage("login-form.html")
		returnme=returnme.replace("%LOGIN_BOX%",login)

	return returnme

def load_cookies():
	try:
		COOKIES=cookies.SimpleCookie()
		COOKIES.load(environ["HTTP_COOKIE"])
		return COOKIES
	except KeyError:
		popup=loadpage("popup.html")
		message="Please enable cookies"
		popup=popup.replace("%MESSAGE%",message)
		print(popup)
		quit()

def sendto(page,message=None):
	print("Content-type: text/html\n")

	if message:
		popup=loadpage("popup.html")
		popup=popup.replace("%MESSAGE%",message)
		print(popup)

	redirect_code=loadpage("redirect.html")
	redirect_code=redirect_code.replace("%GOTO_PAGE%",page)
	print(redirect_code)
