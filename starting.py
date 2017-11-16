import cgi
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


allowed_users=["14bce027@nirmauni.ac.in","14bce040@nirmauni.ac.in","14bce064@nirmauni.ac.in","16bce058@nirmauni.ac.in","15bce114@nirmauni.ac.in","16bce090@nirmauni.ac.in","16bce056@nirmauni.ac.in","16bit048@nirmauni.ac.in","16bit039@nirmauni.ac.in","16bce060@nirmauni.ac.in","16bce059@nirmauni.ac.in","16bce028@nirmauni.ac.in","16bce127@nirmauni.ac.in","16bce057@nirmauni.ac.in","15bce050@nirmauni.ac.in","15bit054@nirmauni.ac.in","15bce131@nirmauni.ac.in","15bce103@nirmauni.ac.in","15bit052@nirmauni.ac.in","15bit003@nirmauni.ac.in","15bit015@nirmauni.ac.in","15bit008@nirmauni.ac.in","15bit024@nirmauni.ac.in","15bit057@nirmauni.ac.in","15bce024@nirmauni.ac.in","15bit063@nirmauni.ac.in","15bit028@nirmauni.ac.in","15bit005@nirmauni.ac.in","16bce060@nirmauni.ac.in","16bit010@nirmauni.ac.in","16bit091@nirmauni.ac.in","15bit054@nirmauni.ac.in","15bit058@nirmauni.ac.in","15bce114@nirmauni.ac.in","15bce041@nirmauni.ac.in","15bce103@nirmauni.ac.in","15bit028@nirmauni.ac.in","15bit015@nirmauni.ac.in","15bit005@nirmauni.ac.in","15bit008@nirmauni.ac.in","15bit032@nirmauni.ac.in","15bit013@nirmauni.ac.in","15bit057@nirmauni.ac.in","15bit058@nirmauni.ac.in","15bit024@nirmauni.ac.in","15bit054@nirmauni.ac.in","15bit057@nirmauni.ac.in","15bit052@nirmauni.ac.in","15bit003@nirmauni.ac.in","15bit050@nirmauni.ac.in","15bit063@nirmauni.ac.in","15bce024@nirmauni.ac.in","15bce050@nirmauni.ac.in","14bce024@nirmauni.ac.in","14bce029@nirmauni.ac.in","14bce030@nirmauni.ac.in","14bce050@nirmauni.ac.in","14bce119@nirmauni.ac.in","14bce127@nirmauni.ac.in"]
showAll_users=["14bce064@nirmauni.ac.in","14bce024@nirmauni.ac.in","14bce029@nirmauni.ac.in","14bce030@nirmauni.ac.in","14bce036@nirmauni.ac.in","14bce050@nirmauni.ac.in","14bce119@nirmauni.ac.in","14bce127@nirmauni.ac.in"]

class MyHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            k=user.nickname()
            if k in allowed_users:
                greeting = ('Welcome, %s!<a href="/NewEntry"> <br><br><br>Go to Home Page</a> <br><br>(<a href="%s">google sign out</a>)' %
                            (user.nickname(),users.create_logout_url('/')))
            else:
                greeting = ('Welcome, You are not allowed to use the site, contact us at pfiger@gmail.com ! (<a href="%s">sign out</a>)' %
                            (users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))

        self.response.out.write('<html><body>%s</body></html>' % greeting)



###################################################################################################################
class NewEntry(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            k=user.nickname()
            if k in allowed_users:
                template = JINJA_ENVIRONMENT.get_template('main.html')
                self.response.write(template.render())
            else:
                greeting=('Welcome, You are not allowed to do data entry, try with nirma account ! (<a href="%s">sign out</a>)' %
                            (users.create_logout_url('/NewEntry')))
                self.response.out.write('<html><body>%s</body></html>' % greeting)
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))
            self.response.out.write('<html><body>%s</body></html>' % greeting)

class Conformation(webapp2.RequestHandler):
    def get(self):self.response.write("oops - worng page")
    def post(self):
        #self.response.write("hhhhhhs")
        regid=self.request.get('regid')
        name=self.request.get('name')
        contactnum=self.request.get('contactnum')
        email=self.request.get('email')
        totalfee=self.request.get('totalfee')
        paid=self.request.get('paid')
        remaining=self.request.get('remaining')
        EVENTS=self.request.get_all('EVENTS')
        WORKSHOPS=self.request.get_all('WORKSHOPS')
        TUTORIALS=self.request.get_all('TUTORIALS')
        template_values={
            'regid' : regid,
            'name': name,
            'contactnum': contactnum,
            'email':email,
            'totalfee': totalfee,
            'paid': paid,
            'remaining': remaining,
            'EVENTS': EVENTS,
            'WORKSHOPS': WORKSHOPS,
        }
        template = JINJA_ENVIRONMENT.get_template('conformation.html')
        self.response.write(template.render(template_values))


class FormData(ndb.Model):
    """Data Entry For Fest"""
    regid = ndb.StringProperty()
    name = ndb.StringProperty()
    contactnum = ndb.StringProperty()
    email = ndb.StringProperty()
    totalfee = ndb.IntegerProperty()
    paid = ndb.IntegerProperty()
    remaining = ndb.IntegerProperty()
    EVENTS = ndb.StringProperty()
    WORKSHOPS = ndb.StringProperty()
    volunteer = ndb.StringProperty()

class SubmitNuForm(webapp2.RequestHandler):
    def get(self):
        self.response.write("ooops - wrong-page")

    def post(self):
        n=self.request.get('name')
        d=FormData()
        d.regid=self.request.get('regid')
        d.name=n
        d.contactnum=self.request.get('contactnum')
        d.email=self.request.get('email')
        d.totalfee=int(self.request.get('totalfee'))
        d.paid=int(self.request.get('paid'))
        d.remaining=int(self.request.get('remaining'))
        EVENTS=""
        c=self.request.get_all('EVENTS')
        for x in c: EVENTS=EVENTS+x+", "
        d.EVENTS=EVENTS
        c=self.request.get_all('WORKSHOPS')
        WORKSHOPS=""
        for x in c: WORKSHOPS=WORKSHOPS+x+", "
        d.WORKSHOPS=WORKSHOPS
        u=users.get_current_user()
        d.volunteer=u.email()
        k=d.put()
        template_values={'key': k,}
        template = JINJA_ENVIRONMENT.get_template('submitted.html')
        self.response.write(template.render(template_values))


###############################################################################################################

class ShowAll(webapp2.RequestHandler):
	def get(self):
		participants_query=FormData.query()
		participants=participants_query.fetch()
#		self.response.write("hello from showAll")
		template_values={'participants': participants }
		template = JINJA_ENVIRONMENT.get_template('showall.html')
		self.response.write(template.render(template_values))
#        self.response.write(template.render(template_values))

	def post(self):
		self.response.write("Helllllo, wrong page... nothing to do here !!")


app = webapp2.WSGIApplication([
    ('/', MyHandler),
	('/NewEntry', NewEntry),
	('/Conformation', Conformation),
	('/Submit',SubmitNuForm),
	('/ShowAll',ShowAll),
], debug=True)
