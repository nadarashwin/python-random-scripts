#!/usr/local/bin/python2.7

import csv
import psutil

##Arguements used in the following 'a' variable is nothing but the parameters which can be passed of 'psutil.Process(j).as_dict' .Ref :-   https://pythonhosted.org/psutil/
a = "pid ppid create_time name status username"
lst = []
for i in psutil.process_iter():
 b = i.as_dict(attrs=["pid"])
 for j in b.values():
  lst.append(psutil.Process(j).as_dict(attrs=a.split()))
  with open('test.csv', 'w') as csv_file:
   writer = csv.DictWriter(csv_file, fieldnames=a.split(), lineterminator='\n')
   writer.writeheader()
   for i in range(0,len(lst)):
    writer.writerow(lst[i])

