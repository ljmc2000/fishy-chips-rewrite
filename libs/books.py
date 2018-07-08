#library for displaying the gross profits

def get_twixt(mycursor, cutoff_time):
	'''fetch entrys from cursor until date'''
	#internal libs
	from functions import loadsubpage

	#external libs
	from html import escape
	import datetime

	row_template=loadsubpage("books_table_row.html")
	returnme=""
	total=0


	while mycursor._have_unread_result():
		if mycursor._nextrow[0]:
			if  mycursor._nextrow[0][2] < cutoff_time:
				break


		orderno,username,placed,spent=mycursor.fetchone()

		#fix the first entry always appearing in the today column
		if placed < cutoff_time:
			mycursor.fetchall()
			mycursor.execute(mycursor._executed)  #execute last
			break

		row=row_template
		row=row.replace("%ORDERNO%", str(orderno) )
		unme=username.decode()
		row=row.replace("%USERNAME%", escape(unme) )
		row=row.replace("%PLACED%", placed.strftime("%d/%m/%Y") )
		row=row.replace("%SPENT%", "€%.2f" % spent )
		returnme=returnme+row
		total=total+spent

	if returnme and total:
		return returnme,total
	else:
		return "",0

def get_books_rows():
	'''return all the books rows and totals for day month and all time'''
	#internal libs
	from database_connection import database_connect

	#external libs
	import datetime

	myconnection,mycursor=database_connect()
	get_fulfilled_orders="select orderno,username,placed,total from valid_orders where fulfilled=1 order by placed desc"
	mycursor.execute(get_fulfilled_orders)

	cutoff_time = datetime.datetime.now().replace(hour=0,minute=0,second=0)
	day_row,day_total=get_twixt(mycursor, cutoff_time)

	cutoff_time = datetime.datetime.now() - datetime.timedelta(days=30)
	month_row,month_total=get_twixt(mycursor, cutoff_time)
	month_total=month_total+day_total

	cutoff_time=datetime.datetime(1,1,1)
	alltime_row,alltime_total=get_twixt(mycursor, cutoff_time)
	alltime_total=alltime_total+month_total


	return day_row,day_total,month_row,month_total,alltime_row,alltime_total
