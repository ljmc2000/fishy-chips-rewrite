#!/usr/bin/python3.5
#cleanup any messes left by the program

#internal libs
from database_connection import database_connect

#external libs
import os

#connect to database
myconnection,mycursor=database_connect()

#ensure food images directory exists
foodir="food_images"
if not os.path.exists(foodir):
	os.mkdirs(foodir)

#get valid filenames from database
mycursor.execute("select picture from food")
pictures=mycursor.fetchall()
for a in range(0,mycursor._rowcount):
	pictures[a]=pictures[a][0].decode()

#delete orphaned photos from disk
for image in os.listdir(foodir):
	if image not in pictures:
		os.remove(foodir+"/"+image)



mycursor.close()
myconnection.close()
