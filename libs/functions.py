#some functions that can be used by all other cgi scripts
from os import environ
from http import cookies

def is_admin():
	'''check if the user is logged in and is an admin'''
	from classes import User

	COOKIES=load_cookies()
	if not COOKIES.get("Login_UID"):
		return False

	user=User(COOKIES["Login_UID"].value)
	return user.username=="admin"

def loadpage(name):
	'''load an entire page template'''
	myfile=open("pages/"+name,"r")
	returnme=myfile.read()
	myfile.close

	return returnme

def loadsubpage(name):
	'''load a shorter html code snippet'''
	myfile=open("subpages/"+name,"r")
	returnme=myfile.read()
	myfile.close

	return returnme

def loadheader():
	returnme=loadsubpage("common_header.html")
	COOKIES=load_cookies()

	if is_admin():
		admin_header=loadsubpage("admin-header.html")
		returnme=returnme.replace("%LOGIN_BOX%",admin_header)

	elif COOKIES.get("Login_UID"):
		logout=loadsubpage("logout-form.html")
		returnme=returnme.replace("%LOGIN_BOX%",logout)
	else:
		login=loadsubpage("login-form.html")
		returnme=returnme.replace("%LOGIN_BOX%",login)

	return returnme

def load_cookies():
	try:
		COOKIES=cookies.SimpleCookie()
		COOKIES.load(environ["HTTP_COOKIE"])
		return COOKIES
	except KeyError:
		popup=loadsubpage("popup.html")
		message="Please enable cookies"
		popup=popup.replace("%MESSAGE%",message)
		print(popup)
		quit()

def sendto(page,message=None):
	declare_http()

	if message:
		popup=loadsubpage("popup.html")
		popup=popup.replace("%MESSAGE%",message)
		print(popup)

	redirect_code=loadsubpage("redirect.html")
	redirect_code=redirect_code.replace("%GOTO_PAGE%",page)
	print(redirect_code)

def declare_http():
	'''instead of putting content-type: text/html in each file individually
	declare it once here and reference it ever after'''
	print("Content-Type: text/html; charset=utf-8\n")
