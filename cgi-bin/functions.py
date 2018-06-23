#some functions that can be used by all other cgi scripts

def loadpage(name):
	myfile=open("pages/"+name,"r")
	returnme=myfile.read()
	myfile.close

	return returnme
