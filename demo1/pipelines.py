# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from demo1.items import BiddingItem
import traceback
from scrapy.exceptions import DropItem
import datetime


# class Demo1Pipeline:
#     def process_item(self, item, spider):
#         return item

ITEM_PIPELINES = {
    'test.pipelines.MongoDBPipelines': 300
}

# def to_date(value):   #把时间戳转换成字符串格式时间
#     otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(value / 1000))
#     return otherStyleTime

def to_date(value):
    otherStyleTime = datetime.datetime.fromtimestamp(value / 1000)
    return otherStyleTime

class MongoDBPipelines(object):
    def __init__(self,mongourl,mongoport,mongodb):
        self.mongourl = mongourl
        self.mongoport = mongoport
        self.mongodb = mongodb

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongourl=crawler.settings.get("MONGO_URL"),
            mongoport=crawler.settings.get("MONGO_PORT"),
            mongodb=crawler.settings.get("MONGO_DB")
        )
    def open_spider(self,spider):    #开启数据库连接
        self.client = pymongo.MongoClient(self.mongourl,self.mongoport)
        self.db = self.client[self.mongodb]



    def process_item(self, item, spider):     #对Item进行处理
        # self.db[item.collection].insert(dict(item))   #insert插入数据
        # time1 = item.get("publish_time")
        # time2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item.get("publish_time") / 1000))
        # item["publish_time"] = time2
        self.db[item.collection].update({'id':item["id"]},dict(item),True)  #update更新数据 → id一致数据不重复传入
        return item


    def close_spider(self, spider):     #关闭数据库连接
        self.client.close()

