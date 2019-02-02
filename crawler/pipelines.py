# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
import datetime
class MongoPipeline(object):

    collection_name = 'youtube_live_stream'

    def __init__(self, mongo_server, mongo_port, mongo_db, mongo_user, mongo_pass):
        self.mongo_server = mongo_server
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db
        self.mongo_user = mongo_user
        self.mongo_pass = mongo_pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_server=crawler.settings.get('MONGO_SERVER'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_user=crawler.settings.get('MONGO_USER'),
            mongo_pass=crawler.settings.get('MONGO_PASS')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_server, self.mongo_port)
        self.db = self.client[self.mongo_db]
        self.db.authenticate(self.mongo_user,self.mongo_pass, mechanism='SCRAM-SHA-1')

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item = dict(item)
        if item['statistics'].get('liveCount') == 0:
            item["snippet"]["liveBroadcastContent"] = "none"
        self.db[self.collection_name].update_one({
            'id' : item['id']
        }, {
            '$set': item,
            '$setOnInsert':{
                'created_time':datetime.datetime.now()
            }
        },upsert=True)
        return item
