#!/usr/local/bin/python2.7
# encoding=utf8






'''
import re
v = "aeiou"
c = "qwrtypsdfghjklzxcvbnm"
m = re.findall(r'(?<=[%s])([%s]{2,})[%s]' %(c,v,c), raw_input(),re.I)
print '\n'.join(m or ['-1'])

'''


'''
import re
m = re.search(r'([a-zA-Z0-9])\1+',raw_input().strip())
print (m.group(1) if m else -1)
'''


'''
import re
print "\n".join(i for i in re.split("[.,]+", raw_input().strip()) if len(i) > 0)
'''

"""
import re
a = int(raw_input())
b = (raw_input() for _ in range(a))
print map(lambda x: bool(re.match(r"^([0-9\+\-\.]+)$",x)), b)

"""



'''
a = int(raw_input())
b= [ map(str,raw_input().split()) for _ in range(a) ]

b.sort(key=lambda x: x[-2])

c = map(lambda x: "Mr. " + x[0] + " " + x[1] if x[-1] == 'M' else "Ms. " + x[0] + " " + x[1], b)
print "\n".join(c)
'''

'''
a = int(raw_input())
b= [ raw_input() for _ in range(a) ]

def func(argu):
	c = []
	for i in range(len(argu)):
		c.append(argu[i][-10:])
	c.sort()
	for i in range(len(argu)):
		print "+91 " + c[i][-10:][:5] + " " + c[i][-10:][5:]

func(b)
'''


'''
import re
reg = re.compile(r"^([a-z]|[A-Z]|[0-9]|[-]|[_])+@([a-z]|[A-Z]|[0-9])+\.([0-9]|[a-z]|[A-Z]){,3}$")
n = int(raw_input())
f = [ raw_input() for _ in range(n)]
print filter(reg.match,f)
'''



'''
row, column = map(int,raw_input().split())
a = [map(int,raw_input().split()) for _ in range(row)]
attr = raw_input()
a.sort(key=lambda x: x[int(attr)])
for i in a:
	print " ".join(map(str,i))

print a, attr

'''