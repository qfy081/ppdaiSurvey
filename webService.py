#encoding=utf8
import os
import tornado.web
import tornado.ioloop
import re

class indexHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
	tornado.web.RequestHandler.__init__( self, *args, **kwargs )
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
			if q.strip('\r\n') == '':
			    continue
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
	self.qs = qs
 
		 
    def get(self):  
	self.post()

    def post(self):  
	self.render('index.html',questions=self.qs)
         





handlers=[
		(r'/',indexHandler),
	#	(r'/getQuestions',getQuestions),
	#	(r'/postAnswers',postAnswers),
		]
settings={
		'static_path':os.path.join(os.path.dirname(__file__),'static'),
		'template_path':os.path.join(os.path.dirname(__file__),'template'),
		}

app=tornado.web.Application(handlers,**settings)
app.listen(8888)
tornado.ioloop.IOLoop.instance().start()
