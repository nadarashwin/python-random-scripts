#!/usr/local/bin/python2.7
# encoding=utf8
from collections import OrderedDict
import MySQLdb
import json

db = MySQLdb.connect(host="",port=,user="",db="",passwd="")
cursor = db.cursor()
cursor.execute("select B.NAME Connector_Name, B.PUBLISHER, B.DESCRIPTION, B.IS_PUBLIC, B.ZIP_FILE_NAME, A.NAME image_name from IOD_FILE_RECORD A,_CONNECTOR B where A.ID=B.IMAGE_RECORD_ID")
first_result = cursor.fetchall()

cursor.execute("select NAME,PUBLISHER,DESCRIPTION,IS_PUBLIC,ZIP_FILE_NAME from IOD_CONNECTOR where IMAGE_RECORD_ID is NULL")
second_result = cursor.fetchall()

cursor.close()

lst =[]
for i in range(len(first_result)):
 lst.append(first_result[i][4])
for i in range(len(second_result)):
 lst.append(second_result[i][4])

dic = {}
for i in range(len(lst)):
 for j in first_result:
  if lst[i] in j:
   dic[lst[i]] = OrderedDict ([ ("name", j[0]), ("publisher", j[1]), ("description", j[2]), ("isPublic", 'true' if ord(j[3])==1 else "false"), ("imageFile",  j[5]) ])
 for k in second_result:
  if lst[i] in k:
   dic[lst[i]] = OrderedDict ([ ("name", k[0]), ("publisher", k[1]), ("description", k[2]), ("isPublic", 'true' if ord(k[3])==1 else "false"), ("imageFile", "informatica_default.jpg") ])

with open('data.json', 'w') as outfile:
    json.dump(dic, outfile, indent=4, separators=(',', ':'),encoding="ISO-8859-1")
    print "output has been written to data.json" 
