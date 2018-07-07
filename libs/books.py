#library for displaying the gross profits

def get_twixt(mycursor, cutoff_time):
	'''fetch entrys from cursor until date'''
	from html import escape
	from functions import loadsubpage
	import datetime

	row_template=loadsubpage("books_table_row.html")
	returnme=""
	total=0


	placed = datetime.datetime.now()
	while (placed > cutoff_time) and ( mycursor._have_unread_result() ):
		orderno,username,placed,spent=mycursor.fetchone()
		row=row_template
		row=row.replace("%ORDERNO%", str(orderno) )
		unme=username.decode()
		row=row.replace("%USERNAME%", escape(unme) )
		row=row.replace("%PLACED%", placed.strftime("%d/%m/%Y") )
		row=row.replace("%SPENT%", "€%.2f" % spent )
		returnme=returnme+row
		total=total+spent

	return returnme,total

def get_books_rows():
	'''return all the books rows and totals for day month and all time'''
	from database_connection import database_connect
	import datetime

	myconnection,mycursor=database_connect()
	get_fulfilled_orders="select orderno,username,placed,total from valid_orders where fulfilled=1 order by placed desc"
	mycursor.execute(get_fulfilled_orders)

	cutoff_time = datetime.datetime.now() - datetime.timedelta(days=1)
	day_row,day_total=get_twixt(mycursor, cutoff_time)

	cutoff_time = datetime.datetime.now() - datetime.timedelta(days=30)
	month_row,month_total=get_twixt(mycursor, cutoff_time)

	cutoff_time=datetime.datetime(1,1,1)
	alltime_row,alltime_total=get_twixt(mycursor, cutoff_time)


	return day_row,day_total,month_row,month_total,alltime_row,alltime_total
