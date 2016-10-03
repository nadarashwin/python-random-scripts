#!/usr/bin/python

import subprocess
from datetime import timedelta, datetime
import re
import smtplib
import time

now = int( time.time() )
ten_days = now - (60 * 60 * 24 * 10)

##define regex to match the time
r = re.compile(r'\w+ \w+ \d+ \d+:\d')

##define a regex to filter the  duble spaces on bash
cd = "s/[[:space:]]\+/ /g"

##define the patterm for time so that we can use it for grep
current_time = "".join(re.findall(r,datetime.now().strftime("%a %b %-d %H:%M:%S %Y")))
two_hours_diff = "".join(re.findall(r,(datetime.now() - timedelta(hours=2)).strftime("%a %b %-d %H:%M:%S %Y")))
one_day_diff = "".join(re.findall(r,(datetime.now() - timedelta(days=1)).strftime("%a %b %-d %H:%M:%S %Y")))
seven_day_diff = "".join(re.findall(r,(datetime.now() - timedelta(days=7)).strftime("%a %b %-d %H:%M:%S %Y")))

##command definition which has to be passed to subprocess
python_comm_curr = "/opt/graphite/bin/whisper-fetch.py AgentCount.wsp --from="+ '"%d"'%ten_days + " --pretty |sed -e "+ '"%s"'%cd + "  |grep " + '"%s"'%current_time + "  |awk {'print $NF'}"
python_comm_2h = "/opt/graphite/bin/whisper-fetch.py AgentCount.wsp --from="+ '"%d"'%ten_days + " --pretty |sed -e "+ '"%s"'%cd + "  |grep " + '"%s"'%two_hours_diff + "  |awk {'print $NF'}"
python_comm_1d = "/opt/graphite/bin/whisper-fetch.py AgentCount.wsp --from="+ '"%d"'%ten_days + " --pretty |sed -e "+ '"%s"'%cd + "  |grep " + '"%s"'%one_day_diff + "  |awk {'print $NF'}"
python_comm_7d = "/opt/graphite/bin/whisper-fetch.py AgentCount.wsp --from="+ '"%d"'%ten_days + " --pretty |sed -e "+ '"%s"'%cd + "  |grep " + '"%s"'%seven_day_diff + "  |awk {'print $NF'}"

file_loca="/opt/graphite/storage/whisper/"
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
        sender = "root@info.com"
        rec = "as@info.com"
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, rec, mess)
        smtpObj.quit()

def logic(curr,prev,args,pod):
        if curr < prev:
                result = abs(curr - prev)/prev*100.0
                if result > 20.0:
                        output = """From: Ashwin(root@graphite_server)
To: as@info.com
Subject: Alert on Nagios

Crtical: The Active agent count in %s dropped by %s from %s average count.
         Current value is %s and %s is %s.
""" % (pod, result, args, curr, args, prev)
                        mail(output)

logic(pod1_result[0],pod1_result[1], "2 hours value", "APP1")
logic(pod1_result[0],pod1_result[2], "1 day value", "APP1")
logic(pod1_result[0],pod1_result[3], "7 days value", "APP1")

logic(pod2_result[0],pod2_result[1], "2 hours value", "APP2")
logic(pod2_result[0],pod2_result[2], "1 day value", "APP2")
logic(pod2_result[0],pod2_result[3], "7 days value", "APP2")

logic(pod3_result[0],pod3_result[1], "2 hours value", "APP3")
logic(pod3_result[0],pod3_result[2], "1 day value", "APP3")
logic(pod3_result[0],pod3_result[3], "7 days value", "APP3")


