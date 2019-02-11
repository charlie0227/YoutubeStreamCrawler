import scrapy
from ..items import LiveStreamItem
import urllib
import json
import datetime
from pymongo import MongoClient
class LiveStats(scrapy.Spider):
    name = "getChannelDetail"
    def __init__(self):
        self.CHANNEL_API = 'https://www.googleapis.com/youtube/v3/channels'
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
                'part':'snippet,statistics',#2
                'id':video['snippet']['channelId'],
                'key':self.GOOGLE_API_KEY
            }
            yield scrapy.Request(
                url=self.CHANNEL_API + '?' + urllib.parse.urlencode(PARAMS),
                callback=self.parse_video,
                errback=self.errback,
                meta=video
            )
    def parse_video(self, response):
        item = response.meta
        obj = json.loads(response.body)
        item['channel'] = obj.get('items')[0]
        item['channel']['statistics']['commentCount'] = int(item['channel']['statistics']['commentCount'])
        item['channel']['statistics']['subscriberCount'] = int(item['channel']['statistics']['subscriberCount'])
        item['channel']['statistics']['videoCount'] = int(item['channel']['statistics']['videoCount'])
        item['channel']['statistics']['viewCount'] = int(item['channel']['statistics']['viewCount'])
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