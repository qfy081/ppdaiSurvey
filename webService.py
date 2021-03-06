#encoding=utf8
import os
import tornado.web
import tornado.ioloop
import re
import MySQLdb
class indexHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
	tornado.web.RequestHandler.__init__( self, *args, **kwargs )
	qs = []
	count = 0
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
			if q.strip('\r\n') == '':
			    continue
			qs.append((q,count,selec))
			count += 1
			preLine = line	
			continue
		    else:
			selec += line
		preLine = line	
	except Exception,e:
	    print e
	
	for q in qs:
	    print q[0]
	
	print len(qs)
	self.qs = qs
 
		 
    def get(self):  
	self.post()

    def post(self):  
	self.render('index.html',questions=self.qs)



db = MySQLdb.connect(host='localhost', user='chenlei', db='test',charset='utf8')         
db.autocommit(1) 
cursor = db.cursor() 
class postAnswers(tornado.web.RequestHandler):

    def get(self):  
	pass

    def post(self):  
	name=self.get_argument('name')
	cell=self.get_argument('cellphone')
	answers = []
	for i in xrange(93):
	    t = self.get_argument('answer'+str(i))
	    answers.append(t)	
	sql = 'insert into survey values("%s","%s","%s");' % (name,cell,'::'.join(answers))
	print sql
	cursor.execute(sql)
	self.render('success.html')


handlers=[
		(r'/',indexHandler),
	#	(r'/getQuestions',getQuestions),
		(r'/postAnswers',postAnswers),
		]
settings={
		'static_path':os.path.join(os.path.dirname(__file__),'static'),
		'template_path':os.path.join(os.path.dirname(__file__),'template'),
		}

app=tornado.web.Application(handlers,**settings)
app.listen(8888)
tornado.ioloop.IOLoop.instance().start()
