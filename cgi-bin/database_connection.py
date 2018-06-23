import mysql.connector	#package mysql-connector is required for this to work

def database_connect():
	try:
		user="webdev"
		password="phprocks"
		host="localhost"
		database= "webdev"
		myconnection=mysql.connector.connect(user=user,password=password,host=host,database=database)
		mycursor=myconnection.cursor(prepared=True)

		return (myconnection,mycursor)
	except:
		print("Content-Type: text/plain\n\ndatabase connection failed")
		quit()

#to get database connection and cursor pass
#connection,cursor=database_connect()
