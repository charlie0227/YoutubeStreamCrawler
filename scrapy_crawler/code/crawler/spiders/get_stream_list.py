import scrapy
from ..items import LiveStreamItem
import urllib
import json
import datetime
import logging
from pymongo import MongoClient
class StreamList(scrapy.Spider):
    name = "getStreamList"
    def __init__(self):
        self.PLAYLIST_API = 'https://www.googleapis.com/youtube/v3/playlistItems'
        self.VIDEO_API = 'https://www.googleapis.com/youtube/v3/videos'
    def start_requests(self):
        self.GOOGLE_API_KEY = self.settings.get('GOOGLE_API_KEY')
        playlists = [
            'PLiCvVJzBupKnkb9LxWGIUfzWl8-LVxb2N',# Gaming
            'PL8fVUTBmJhHKLxxqAxVf3eEVitZr_fbQZ',# Sport
            'PL57quI9usf_v_OqFuXASZ8ObdCO8_7n_h',# Tech
            'PLIFqWCuxNyogIPGTCQAGmPoghZRnP3r0b',# Animal
            'PLU12uITxBEPGpwevoL7K3El-y1zarYRzM',# Mobile
            'PLU12uITxBEPHAEA9JChLuj0uRglw-doC3',# Web cam
        ]
        for playlistId in playlists:
            # PLAYLIST
            PARAMS = {
                'part':'contentDetails',#2
                'maxResults':50,
                'playlistId':playlistId,
                'key':self.GOOGLE_API_KEY
            }
            yield scrapy.Request(
                url=self.PLAYLIST_API + '?' + urllib.parse.urlencode(PARAMS), 
                callback=self.parse_playlist, 
                errback=self.errback, 
                meta=PARAMS
            )

    def parse_playlist(self, response):
        obj = json.loads(response.body)
        for i in obj['items']:
            # VIDEO
            PARAMS = {
                'part':'id,snippet,contentDetails,status',
                'id':i['contentDetails']['videoId'],
                'key':self.GOOGLE_API_KEY,
                'hl':'zh-TW'
            }
            yield scrapy.Request(
                url=self.VIDEO_API + '?' + urllib.parse.urlencode(PARAMS),
                callback=self.parse_video,
                errback=self.errback, 
                meta=PARAMS
            )
        # PLAYLIST NEXT PAGE
        if obj.get('nextPageToken'):
            self.log(response.meta,level=logging.INFO)
            PARAMS = response.meta
            PARAMS['pageToken'] = obj.get('nextPageToken')
            yield scrapy.Request(
                url=self.PLAYLIST_API + '?' + urllib.parse.urlencode(PARAMS),
                callback=self.parse_playlist,
                errback=self.errback,
                meta=PARAMS
            )
    def parse_video(self, response):
        obj = json.loads(response.body)
        video = obj.get('items')[0]
        item = LiveStreamItem()
        item['id'] = video.get('id')
        item['snippet'] = video.get('snippet')
        item['status'] = video.get('status')
        item['contentDetails'] = video.get('contentDetails')
        item['statistics'] = {}
        item['last_update'] = datetime.datetime.now()
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