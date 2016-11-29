#!/usr/local/bin/python2.7
# encoding=utf8
import MySQLdb
import json

db = MySQLdb.connect(host="",port=,user="",db="",passwd="")
cursor = db.cursor()
cursor.execute("select B.NAME Connector_Name, B.PUBLISHER, B.DESCRIPTION, B.IS_PUBLIC, B.ZIP_FILE_NAME, A.NAME image_name from IMAGE A,CONNECTOR B where A.ID=B.IMAGE_RECORD_ID")
b = cursor.fetchall()

lst =[]
for i in range(len(b)):
 lst.append(b[i][4])

dic = {}
for i in range(len(lst)):
 for j in b:
  if lst[i] in j:
   dic[lst[i]] = {"name": j[0], "publisher": j[1], "description": j[2], "isPublic": 'true' if ord(j[3])==1 else "false","imageFile": j[5]}

with open('data.json', 'w') as outfile:
    json.dump(dic, outfile, indent=4, sort_keys=True, separators=(',', ':'),encoding="ISO-8859-1")
    print "output has been written to data.json" 
