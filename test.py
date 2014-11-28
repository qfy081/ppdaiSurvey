#encoding=utf8
import re
qs = []
try:
    fi = open('survey.txt')
    selec = ''
    q = ''
    preLine = ''
    for line in fi:
	if re.match(r'\d+、',line):
	    selec = ''
	    q = line
	else:
	    if line.strip('\r\n') == '' and preLine.strip('\r\n').strip() != '':
		qs.append((q,selec))
		preLine = line	
		continue
	    else:
		selec += line
	preLine = line	
except Exception,e:
    print e

for q in qs:
    print q[0]
