#!/usr/bin/python3.5
#view gross profits for the business

#internal libs
from functions import *
from books import get_books_rows

#check admin
if not is_admin():
	sendto("/",message="access_denied")
	quit()

#genderate page
pagestring=loadpage("view-books.html")
pagestring=pagestring.replace("%COMMON_HEADER%",loadheader() )

day_row,day_total,month_row,month_total,alltime_row,alltime_total=get_books_rows()
pagestring=pagestring.replace("%DAY_ROWS%",day_row)
pagestring=pagestring.replace("%DAY_TOTAL%", "€%.2f" % day_total)
pagestring=pagestring.replace("%MONTH_ROWS%",month_row)
pagestring=pagestring.replace("%MONTH_TOTAL%", "€%.2f" % month_total)
pagestring=pagestring.replace("%ALLTIME_ROWS%",alltime_row)
pagestring=pagestring.replace("%ALLTIME_TOTAL%", "€%.2f" % alltime_total)

#send page to user
declare_http()
print(pagestring)
