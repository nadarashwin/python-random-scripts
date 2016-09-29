#!/usr/bin/python

import time
import socket
import subprocess

_ssh_server=""
_ssh_user=""
_ssh_pod1_path=""
_ssh_pod2_path=""
_ssh_pod3_path=""
_graphite_server=""
_graphite_port=""
_timestamp= int(time.time())
_metric_name=""

c = "ssh " + _ssh_user + "@" + _ssh_server + " cat " + _ssh_pod1_path + ";" + "echo" + ";" + " cat " + _ssh_pod2_path + ";" + "echo"  + ";" + " cat " + _ssh_pod3_path + ";"

result = []
pod = ["pod1.", "pod2.", "pod3."]
ssh = subprocess.Popen(c.split(), stdout=subprocess.PIPE,universal_newlines=True)
for line in ssh.stdout:
        result.append(line)
        sock = socket.socket()
        sock.connect((_graphite_server,_graphite_port))
        for i in range(0,len(result)):
                metric_name = pod[i] + _metric_name
                message = "%s %d %d\n" %  (metric_name, int(result[i]), _timestamp)
                sock.sendall(message)
        sock.close()

