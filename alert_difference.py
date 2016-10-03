#!/usr/bin/python

import subprocess
from datetime import timedelta, datetime
import re
import smtplib
import time

##By default whisper-fetch will only fetch from past 24 hours so generated a variable ten_days which will fetch from past 10 days
now = int( time.time() )
ten_days = now - (60 * 60 * 24 * 10)

##defineing regex to match the time
r = re.compile(r'\w+ \w+ \d+ \d+:\d')

current_time = "".join(re.findall(r,datetime.now().strftime("%a %b %d %H:%M:%S %Y")))
two_hours_diff = "".join(re.findall(r,(datetime.now() - timedelta(hours=2)).strftime("%a %b %d %H:%M:%S %Y")))
one_day_diff = "".join(re.findall(r,(datetime.now() - timedelta(days=1)).strftime("%a %b %d %H:%M:%S %Y")))
seven_day_diff = "".join(re.findall(r,(datetime.now() - timedelta(days=7)).strftime("%a %b %d %H:%M:%S %Y")))


python_comm_curr = "/opt/graphite/bin/whisper-fetch.py AgentCount.wsp --from="+ '"%d"'%ten_days + " --pretty  |grep " + '"%s"'%current_time + "  |awk {'print $NF'}"
python_comm_2h = "/opt/graphite/bin/whisper-fetch.py AgentCount.wsp --from="+ '"%d"'%ten_days + " --pretty  |grep " + '"%s"'%two_hours_diff + "  |awk {'print $NF'}"
python_comm_1d = "/opt/graphite/bin/whisper-fetch.py AgentCount.wsp --from="+ '"%d"'%ten_days + " --pretty  |grep " + '"%s"'%one_day_diff + "  |awk {'print $NF'}"
python_comm_7d = "/opt/graphite/bin/whisper-fetch.py AgentCount.wsp --from="+ '"%d"'%ten_days + " --pretty  |grep " + '"%s"'%seven_day_diff + "  |awk {'print $NF'}"


file_loca="/opt/graphite/storage/whisper/"
##number of datacenter
pod = ["pod1", "pod2", "pod3"]
#time_con = [python_comm_curr, python_comm_2h, python_comm_1d, python_comm_7d]
time_con = [python_comm_curr, python_comm_2h, python_comm_1d]
pod1_result = []
pod2_result = []
pod3_result = []

for i in range(0,len(time_con)):
	for j in range(0,len(pod)):
		ssh = subprocess.Popen(time_con[i],cwd=file_loca + pod[j], stdout=subprocess.PIPE, shell=True)
		for line in ssh.stdout:
			if j == 0:
				pod1_result.append(float(line.rstrip()))
			elif j == 1:
				pod2_result.append(float(line.rstrip()))
			else:
				pod3_result.append(float(line.rstrip()))


def mail(mess):
	sender = ""
	rec = "" 
	smtpObj = smtplib.SMTP('localhost')
	smtpObj.sendmail(sender, rec, mess)
	smtpObj.quit()
	
def logic(curr,prev,args):
	if curr < prev:
                result = abs(curr - prev)/prev*100.0
                if result > 20.0:
                        output = """From: From(root@graphite_server)
To: root@host-server
Subject: alerting

Crtical: Current value is %s which is lower than %s for  %s  by  %s
""" % (curr, prev, args, result)
			mail(output)


logic(pod1_result[0],pod1_result[1], "2 hours value (POD1):")
logic(pod1_result[0],pod1_result[2], "1 day value (POD1):")
logic(pod1_result[0],pod1_result[3], "7 days value (POD1):")

logic(pod2_result[0],pod2_result[1], "2 hours value (POD2):")
logic(pod2_result[0],pod2_result[2], "1 day value (POD2):")
logic(pod2_result[0],pod2_result[3], "7 days value (POD2):")
        
logic(pod3_result[0],pod3_result[1], "2 hours value (POD3):")
logic(pod3_result[0],pod3_result[2], "1 day value (POD3):")
logic(pod3_result[0],pod3_result[3], "7 days value (POD3):")



'''
if pod1_result[0] == pod1_result[1]:
	print "current :" + pod1_result[0] + ":and 2hours value :" + pod1_result[1] + ":are same"
elif pod1_result[0] > pod1_result[1]:
	print "current :" + pod1_result[0] + ":is greater than 2hours value :" + pod1_result[1]
else:
	result = abs(pod1_result[0] - pod1_result[1])/pod1_result[1]*100.0
	if result > 20.0:
		print "Crtical: Currnt value is:" + pod1_result[0] + ": which is lower then 2 hours value :" + pod1_result[1] + ": by " + str(result) 
	else:
		print "Warning: Currnt value is:" + pod1_result[0] + ": which is lower then 2 hours value: " + pod1_result[1] + ": by " + str(result)

'''

'''
for i in range(0,len(pod)):
	ssh = subprocess.Popen(python_comm_curr,cwd=file_loca + pod[i], stdout=subprocess.PIPE, shell=True)
	for line in ssh.stdout:
		curr_result.append(line)

for i in range(0,len(pod)):
        ssh = subprocess.Popen(python_comm_2h,cwd=file_loca + pod[i], stdout=subprocess.PIPE, shell=True)
        for line in ssh.stdout:
                2h_result.append(line)

for i in range(0,len(pod)):
        ssh = subprocess.Popen(python_comm_1d,cwd=file_loca + pod[i], stdout=subprocess.PIPE, shell=True)
        for line in ssh.stdout:
                1d_result.append(line)

for i in range(0,len(pod)):
        ssh = subprocess.Popen(python_comm_7d,cwd=file_loca + pod[i], stdout=subprocess.PIPE, shell=True)
        for line in ssh.stdout:
                7d_result.append(line)
'''
