import scrapy
from ..items import LiveStreamItem
import urllib
import json
import datetime
from pymongo import MongoClient
class LiveStats(scrapy.Spider):
    name = "getLiveStats"
    def __init__(self):
        self.LIVE_API = 'https://www.youtube.com/live_stats'
        self.collection_name = 'youtube_live_stream'
    def db_connection(self):
        mongo_server = self.settings.get('MONGO_SERVER'),
        mongo_port = self.settings.get('MONGO_PORT'),
        mongo_db = self.settings.get('MONGO_DATABASE'),
        mongo_user = self.settings.get('MONGO_USER'),
        mongo_pass = self.settings.get('MONGO_PASS')
        self.client = MongoClient(mongo_server[0], mongo_port[0])
        self.db = self.client[mongo_db[0]]
        self.db.authenticate(mongo_user[0], mongo_pass, mechanism='SCRAM-SHA-1')
        
    def start_requests(self):
        self.GOOGLE_API_KEY = self.settings.get('GOOGLE_API_KEY')
        self.db_connection()
        for video in self.db[self.collection_name].find({"snippet.liveBroadcastContent":"live"}):
            PARAMS = {
                'v':video['id'],
            }
            yield scrapy.Request(
                url=self.LIVE_API + '?' + urllib.parse.urlencode(PARAMS), 
                callback=self.parse_live, 
                errback=self.errback, 
                meta=video
            )
    def parse_live(self, response):
        item = response.meta
        item['statistics']['liveCount'] = json.loads(response.body)
        item['last_update'] = datetime.datetime.now()
        del(item['created_time'])
        return item
    def errback(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)