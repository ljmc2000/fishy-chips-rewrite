from database_connection import database_connect

class User:
	def __init__(self,uid):
		(myconnection,mycursor)=database_connect()
		get_user_details="select username from users join logged_in_users using (username) where(Login_UID=?)"
		mycursor.execute(get_user_details,(uid,))

		username, = mycursor.fetchone()
		mycursor.close()
		myconnection.close()

		self.username=username.decode()


	def __str__(self):
		return self.username

class CreditCard:
	def __init__(self,user):
		(myconnection,mycursor)=database_connect()
		get_credit_card="select cardnumber, expiremonth, expireyear, ccv from payinfo where (username=?)"
		mycursor.execute(get_credit_card,(user,))

		cardnumber, expiremonth, expireyear, ccv = mycursor.fetchone()
		mycursor.close()
		myconnection.close()

		self.cardnumber=cardnumber.decode()
		self.expiremonth=expiremonth.decode()
		self.expireyear=expireyear
		self.ccv=ccv

	def __str__(self):
		returnme=""
		returnme=returnme+"card_number: "+self.cardnumber+"\n"
		returnme=returnme+"expires: "+self.expiremonth+"/"+str(self.expireyear)+"\n"
		returnme=returnme+"CCV: "+str(self.ccv)
		return returnme

class Address:
	def __init__(self,user):
		(myconnection,mycursor)=database_connect()
		get_address="select line1, line2, town, eircode from address where (username=?)";
		mycursor.execute(get_address,(user,))

		line1, line2, town, eircode = mycursor.fetchone()
		mycursor.close()
		myconnection.close()

		self.line1=line1.decode()
		self.line2=line2.decode()
		self.town=town.decode()
		self.eircode=eircode.decode()

	def __str__(self):
		returnme=""
		returnme=returnme+self.line1+"\n"
		returnme=returnme+self.line2+"\n"
		returnme=returnme+self.town+"\n"
		returnme=returnme+self.eircode
		return returnme

class Buyer(User):
	def __init__(self,uid):
		self=User(uid)
		self.address=Address(self.username)
		self.card=CreditCard(self.username)

	def __str__(self):
		returnme=super.__str__()+"\n"
		returnme=returnme+str(self.card)+"\n"
		returnme=returnme+str(self.address)
