import cookielib
import datetime
import requests
from cms.models import Event
from feed import FeedResource
from bs4 import BeautifulSoup

class ZipEventAppFeedResource(FeedResource):

    web_url = 'https://www.zipeventapp.com/'
    resources = (
        ('get_event_list', Event),
    )

    def prepare(self):

        self.cookies = cookielib.CookieJar()

        self.session = requests.Session()

        r = self.session.get(self.web_url, verify=False, cookies=self.cookies)

        self.cookies = r.cookies
        self.token = r.cookies['__RequestVerificationToken']
        print 'bbbb'
        #self.cookies = r.cookies

        #soup = BeautifulSoup(r.text, 'html.parser')
        #self.token = soup.find(attrs={'name': '__RequestVerificationToken'}).get('value')
        #print self.token
        #print 'vvvvvv'


    def get_event_list(self):


        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            '__RequestVerificationToken': self.token,
            #'Cookie': '__RequestVerificationToken = %s' % self.token
        }
        r = self.session.post(
            'https://www.zipeventapp.com/Event/Search',
            data={'name': 'startup'},
            headers=headers,
            cookies=self.cookies,
            verify=False
        )
        print headers
        print r
        print r.raise_for_status()

    def map_object(self, obj, data):
        start_date, start_time = data['startdate'].split('T')
        end_date, end_time = data['enddate'].split('T')

        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        time = '%s - %s' % (start_time, end_time)

        obj.title = data['name']
        obj.location = data['venue']
        obj.start_date = start_date
        obj.end_date = end_date
        obj.time = time
        #obj.image = data['logo'] # todo
        obj.homrpage_url = data['full_url']
        obj.uuid = data['id']